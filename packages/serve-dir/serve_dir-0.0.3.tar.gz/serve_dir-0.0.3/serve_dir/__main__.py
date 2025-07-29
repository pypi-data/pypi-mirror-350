from .main import Main, arg, flag, _arg_fields
from .server import serve_dir


class App(Main):
    root_dir: str = arg(
        "The root directory", metavar="DIR", default=".", required=False
    )
    cgi: bool = flag("cgi", "use cgi script", default=None)
    byte_range: bool = flag("byte-range", "use byte range", default=None)
    port: int = flag("p", "set port", metavar="NUMBER", default=8058)
    bind: str = flag("b", "bind to address", metavar="X.X.X.X", default="0.0.0.0")

    def start(self) -> None:
        serve_dir(self.__dict__)


def main():
    """CLI entry point."""
    App().main()


(__name__ == "__main__") and main()
