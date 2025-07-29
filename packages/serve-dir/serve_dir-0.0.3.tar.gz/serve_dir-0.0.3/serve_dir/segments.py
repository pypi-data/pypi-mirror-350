from os import fstat, stat


def get_file_stream(path):
    if ".parts.json." in path:
        f = Segments(path)
        return (f, f.length, stat(path).st_mtime)
    else:
        f = open(path, "rb")
        s = fstat(f.fileno())
        return (f, s.st_size, s.st_mtime)


class Segments(object):
    length = 0
    pos = 0

    def __init__(self, src):
        from os.path import realpath, abspath, dirname

        self.length = 0
        self.pos = 0
        with open(src, "rb") as h:
            from json import load

            m = load(h)
            folder = dirname(realpath(abspath(src)))
            self.length = m["length"]
            self.parts = sorted([x[0], x[1], resolve_source(x[2], folder), None] for x in m["parts"])
        from os import environ

        x = environ.get("SEGMENTS_DEBUG")
        if x:
            from sys import stdout

            self.log = stdout.write
        else:
            self.log = lambda *x: None

    def tell(self):
        # assert self.pos < self.length
        assert self.pos >= 0
        return self.pos

    def close(self):
        out = self.log
        for x in self.parts:
            f = x[3]
            if f:
                out("DONE %s-%s %r\n" % (x[0], x[1], x[3]))
                x[3] = f.close() and None
        self.pos = 0
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for x in self.parts:
            (_, _, _, f) = x
            if f:
                # self.log(f"close {x[0:3]}\n")
                f.close()

    def seek(self, offset, whence=0):
        # assert self.pos < self.length
        assert self.pos >= 0
        if whence == 0:
            assert offset < self.length
            assert offset >= 0
            new_pos = self.pos = offset
        elif whence == 1:
            assert (self.pos + offset) < self.length
            assert (self.pos + offset) >= 0
            new_pos = self.pos = self.pos + offset
        elif whence == 2:
            assert (self.length + offset) < self.length
            assert (self.length + offset) >= 0
            new_pos = self.pos = self.length + offset
        else:
            assert 0
        return new_pos

    def read(self, n=-1):
        out = self.log
        if n == 0:
            return b""
        elif n < 0:  # Read until EOF if n is negative
            n = self.length - self.pos

        out(f"read n={n}\n")
        # pos = self.pos
        assert self.pos >= 0
        result: bytearray | None = None
        for x in self.parts:
            out(f"parts {x!r} n={n} pos={self.pos}\n")
            (s, e, path, f) = x
            assert e > s
            if self.pos >= s and self.pos < e:
                seek = self.pos - s
                size = min(e - self.pos, n)
                if not f:
                    out("OPEN %s-%s %r\n" % (x[0], x[1], x[2]))
                    x[3] = f = open(path, "rb")
                f.seek(seek)
                b = f.read(size)
                size = len(b)
                self.pos += size
                n -= size
                out("RET %r\n" % ((self.pos, n, b, size),))
                if result is None:
                    result = bytearray()
                result.extend(b)
            else:
                if f:
                    out("done %s-%s %r\n" % (x[0], x[1], x[3]))
                    x[3] = f.close() and None
        if result is None:
            if self.pos < self.length:
                # out("hole %s-%s\n" % (pos, pos + n))
                size = min(self.length - self.pos, n)
                self.pos += size
                return b"\x00" * size
            return b""
        else:
            return bytes(result)


from os.path import isabs, abspath, normpath, join
from urllib.request import url2pathname
from urllib.parse import urlparse


def resolve_source(uri, dirParent, pathIdTup=None):
    # (scheme, netloc, path, params, query, fragment)
    url = urlparse(uri)
    path = url2pathname(url[2])
    if isabs(path):
        path = abspath(path)
    else:
        path = normpath(join(dirParent, path))
    if pathIdTup:
        return (path, url[5])
    return path
