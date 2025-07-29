from re import compile as regex
from io import BytesIO
from urllib.parse import urlsplit, urlunsplit, unquote
from sys import getfilesystemencoding
from os import listdir, stat
from os.path import isdir, join, exists
from stat import S_ISDIR, S_ISLNK
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer
import datetime

from .segments import get_file_stream
from .utils import dir_listing

try:
    from email.utils import parsedate_to_datetime
except ImportError:
    parsedate_to_datetime = None


BYTE_RANGE_RE = regex(r"bytes=(\d+)?-(\d+)?$")


def parse_byte_range(byte_range: str):
    if byte_range.strip() == "":
        return None, None
    m = BYTE_RANGE_RE.match(byte_range)
    if not m:
        raise ValueError("Invalid byte range %s" % byte_range)
    first, last = [int(x) if x else 0 for x in m.groups()]
    # if last and last < first:
    # 	raise ValueError('Invalid byte range %s' % byte_range)
    return first, last


def copy_byte_range(infile, outfile, start=None, stop=None, bufsize=16 * 1024):
    if start is not None:
        infile.seek(start)
    while 1:
        to_read = min(bufsize, stop + 1 - infile.tell() if stop else bufsize)
        buf = infile.read(to_read)
        if not buf:
            break
        outfile.write(buf)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    def get_res_path(self, name):
        from os.path import join, exists

        for d in self.res_path:
            f = join(d, name)
            if exists(f):
                return f

    def __getattr__(self, name):
        if 0:
            pass
        # elif name == 'dir_script':
        # 	self.__dict__[name] = self.get_res_path("serve_dir.js")
        # elif name == 'dir_style_sheet':
        # 	self.__dict__[name] = self.get_res_path("serve_dir.css")
        elif name == "res_path":
            self.__dict__[name] = set()
        else:
            try:
                return super(ThreadingSimpleServer, self).__getattr__(name)
            except Exception:
                raise AttributeError(name)
        return self.__dict__[name]


class RangeRequestHandler(SimpleHTTPRequestHandler):
    def copyfile(self, source, outputfile):
        try:
            if not self.range:
                return SimpleHTTPRequestHandler.copyfile(self, source, outputfile)
            start, stop = self.range  # set in send_head()
            copy_byte_range(source, outputfile, start, stop)
        except (ConnectionResetError, BrokenPipeError) as e:
            self.log_error("%s %r", e.__class__.__name__, getattr(self, "path", None))

    def send_head(self):
        self.range = None
        path = self.translate_path(self.path)
        # print(path)
        f = None
        if isdir(path):
            parts = urlsplit(self.path)
            if not parts.path.endswith("/"):
                # redirect browser - doing basically what apache does
                self.send_response(301)  # MOVED_PERMANENTLY
                new_parts = (parts[0], parts[1], parts[2] + "/", parts[3], parts[4])
                new_url = urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = join(path, index)
                if exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        # check for trailing "/" which should return 404. See Issue17324
        # The test for this was added in test_httpserver.py
        # However, some OS platforms accept a trailingSlash as a filename
        # See discussion on python-dev and Issue34711 regarding
        # parseing and rejection of filenames with a trailing slash
        if path.endswith("/"):
            self.send_error(404, "File not found")  # NOT_FOUND
            return None
        ########
        if "Range" in self.headers:
            try:
                self.range = parse_byte_range(self.headers["Range"])
            except ValueError:
                self.send_error(400, "Invalid byte range")
                return None
            first, last = self.range
            # print("Range", self.range)
            # Mirroring SimpleHTTPServer.py here
            path = self.translate_path(self.path)
            f = None
            ctype = self.guess_type(path)
            try:
                (f, file_len, mtime) = get_file_stream(path)
            except IOError:
                self.send_error(404, "File not found")
                return None

            if first >= file_len:
                self.send_error(
                    416,
                    "Requested Range Not Satisfiable %r"
                    % ((first, last, file_len, self.headers["Range"]),),
                )
                self.send_header("Content-Range", "bytes */%s" % (file_len,))
                self.send_header("Content-type", ctype)
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Last-Modified", self.date_time_string(mtime))
                self.end_headers()
                return None

            self.send_response(206)
            self.send_header("Content-type", ctype)
            self.send_header("Accept-Ranges", "bytes")

            if last is None or last >= file_len:
                last = file_len - 1
            response_length = last - first + 1

            self.send_header(
                "Content-Range", "bytes %s-%s/%s" % (first, last, file_len)
            )
            self.send_header("Content-Length", str(response_length))
            self.send_header("Last-Modified", self.date_time_string(mtime))
            self.end_headers()
            return f
        ########
        try:
            (f, file_len, mtime) = get_file_stream(path)
        except OSError:
            self.send_error(404, "File not found")  # NOT_FOUND
            return None

        try:
            # Use browser cache if possible
            if (
                parsedate_to_datetime
                and "If-Modified-Since" in self.headers
                and "If-None-Match" not in self.headers
            ):
                # compare If-Modified-Since and time of last file modification
                try:
                    ims = parsedate_to_datetime(self.headers["If-Modified-Since"])
                except (TypeError, IndexError, OverflowError, ValueError):
                    # ignore ill-formed values
                    pass
                else:
                    if ims.tzinfo is None:
                        # obsolete format with no timezone, cf.
                        # https://tools.ietf.org/html/rfc7231#section-7.1.1.1
                        ims = ims.replace(tzinfo=datetime.timezone.utc)
                    if ims.tzinfo is datetime.timezone.utc:
                        # compare to UTC datetime of last modification
                        last_modif = datetime.datetime.fromtimestamp(
                            mtime, datetime.timezone.utc
                        )
                        # remove microseconds, like in If-Modified-Since
                        last_modif = last_modif.replace(microsecond=0)

                        if last_modif <= ims:
                            self.send_response(304)  # NOT_MODIFIED
                            self.end_headers()
                            f.close()
                            return None

            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(file_len))
            self.send_header("Last-Modified", self.date_time_string(mtime))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            return f
        except Exception:
            f.close()
            raise

    def directory_links(self, path):
        q = path.rfind("?")
        h = path.rfind("#", 0, q)
        if h >= 0:
            q = h
        if q < 0:
            s = path.rstrip("/").split("/")
            q = None
        else:
            s = path[0:q].rstrip("/").split("/")
            q = path[q:]
        if not s:
            return [(path, None)]
        i = 0
        j = len(s)
        while j > 0:
            j -= 1
            if j == 0:
                s[i] = (s[i] + "/", "." + (q or ""))
            # elif i == 0:
            # 	s[i] = ('/', '.')
            else:
                s[i] = (s[i] + "/", "../" * j)
            i += 1
        return s

    def list_directory(self, path):

        def statx(path):
            try:
                return stat(path)
            except (FileNotFoundError,) as e:
                self.log_error(
                    "%s %r", e.__class__.__name__, getattr(self, "path", None)
                )
            # except:
            # 	pass

        files = [y for y in ((x, statx(join(path, x))) for x in listdir(path)) if y[1]]
        files.sort(key=lambda a: (not S_ISDIR(a[1].st_mode), a[0].lower()))
        # print(files)
        # r = []
        try:
            displaypath = unquote(self.path, errors="surrogatepass")
        except UnicodeDecodeError:
            displaypath = unquote(path)
        enc = getfilesystemencoding()

        def itemf(v):
            (name, st) = v
            # fullname = join(path, name)
            mode = st.st_mode
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if S_ISDIR(mode):
                displayname = name + "/"
                linkname = name + "/"
            elif S_ISLNK(mode):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            return displayname, linkname

        encoded = "".join(
            dir_listing(
                title=displaypath,
                enc=enc,
                dirs=(
                    (unquote(name), href)
                    for (name, href) in self.directory_links(self.path)
                ),
                items=map(itemf, files),
            )
        ).encode(enc, "surrogateescape")

        f = BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f


def serve_dir(env):
    from os import environ
    from sys import stderr
    from logging import info
    from http.server import CGIHTTPRequestHandler

    out = stderr.write
    env.setdefault("port", int(environ.get("PORT", 8058)))
    env.setdefault("bind", "0.0.0.0")
    if env.get("byte_range") is not False:
        if env.get("cgi", True):

            class CGIRangeRequestHandler(CGIHTTPRequestHandler, RangeRequestHandler):
                def send_head(self):
                    if self.is_cgi():
                        return self.run_cgi()
                    else:
                        try:
                            return RangeRequestHandler.send_head(self)
                        except (ConnectionResetError, BrokenPipeError) as e:
                            self.log_error(
                                "%s %r",
                                e.__class__.__name__,
                                getattr(self, "path", None),
                            )

            Handler = CGIRangeRequestHandler
        else:
            Handler = RangeRequestHandler
    elif env.get("cgi", True):
        Handler = CGIHTTPRequestHandler
    else:
        Handler = SimpleHTTPRequestHandler
    httpd = ThreadingSimpleServer((env["bind"], env["port"]), Handler)
    from os import getcwd, chdir
    from os.path import realpath, dirname, abspath

    d = realpath(abspath(__file__))
    info("res {!r}".format(d))
    httpd.res_path.add(dirname(d))
    x = env.get("root_dir")
    x and chdir(x)
    d = realpath(getcwd())
    httpd.res_path.add(d)
    info("cwd {!r}".format(d))
    Handler.protocol_version = env.get("protocol", "HTTP/1.0")
    serve_message = "{klass} Serving {protocol} on http://{host}:{port}/ ...\n"
    sa = httpd.socket.getsockname()
    out(
        serve_message.format(
            klass=Handler.__name__,
            host=sa[0],
            port=sa[1],
            protocol=Handler.protocol_version,
        )
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        out("\n\nKeyboard interrupt received, exiting.")
