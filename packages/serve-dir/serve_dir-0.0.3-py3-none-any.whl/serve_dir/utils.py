from html import escape as A


def dir_listing(title, dirs, items, enc):

    def C(s):
        return A(s, False)

    yield (
        "<!DOCTYPE html>"
        "<html><head>"
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f'<meta http-equiv="Content-Type" content="text/html; charset={A(enc)}"/>'
        f"<title>{C(title)}</title>"
    )
    yield (
        "<style>"
        "ul,menu,dir{"
        "display:block;"
        "list-style-type:none;"
        "}"
        "ul,ol>li{"
        "background-color:yellowgreen;"
        "}"
        "ul,ol>li>a{"
        "min-height:3rem;"
        "max-height:5rem;"
        "display:block;"
        "overflow-y:hidden;"
        "text-decoration-line:none;"
        "padding:0.25rem 0.25rem;"
        "}"
        "ul,ol>li>a:focus{"
        "color:red;"
        "}"
        "ul,ol>li:hover>a{"
        "color:blue;"
        "}"
        "ul,ol>li:nth-child(even){"
        "background-color:wheat;"
        "}"
        "body>h1>a{"
        "text-decoration-line: none;"
        "min-width:2rem;"
        "min-height:2rem;"
        "display:inline-block;"
        "border-bottom:solid 0.125rem brown;"
        "text-align:center;"
        "margin-left:0.33rem;"
        "}"
        "body>h1{"
        "background-color:azure;"
        "margin:0px;"
        "border-bottom:solid 0.125rem grey;"
        "padding:0.3rem 0.4rem;"
        "}"
        "body>ol{"
        "margin:0px;"
        "border-bottom:solid grey .125rem;"
        "}"
        "body {"
        "margin:0px;"
        "font-family:sans-serif;"
        "}"
        "ol>li::marker{"
        "font-size:small;"
        "font-family:monospace;"
        "}"
        "ol:empty{"
        'content:"Empty";'
        "color:slategray;"
        "}"
        "</style>"
        "</head>"
        "<body>"
    )
    yield "<h1>"
    for name, href in dirs:
        yield f'<a href="{A(href)}">{C(name)}</a>'
    yield "</h1>"
    yield "<ol>"
    for name, href in items:
        yield f'<li><a href="{A(href)}">{C(name)}</a></li>'
    yield "</ol>"
    yield "</body></html>"
