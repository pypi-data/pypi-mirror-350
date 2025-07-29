# miniroute/miniroute.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, ClassVar


class MiniRouter:
    """ Router for miniroute server.
    routes: dict[(method: str, path: str)] -> Callable
    """
    def __init__(self) -> None:
        self.routes = {}

    def _add(self, method: str, path: str, func: Callable) -> None:
        """ Add a new route to the routes map dict. """
        self.routes[(method.upper(), path)] = func

    def dispatch(self, method: str, path: str) -> Callable | None:
        """ Simple dispatcher to register the routes. """
        return self.routes.get((method.upper(), path), None)

    def get(self, path: str) -> Callable:
        """ decorator for post request. """
        def wrapper(func):
            self._add("GET", path, func)
            return func
        return wrapper

    def post(self, path: str) -> Callable:
        """ decorator for post request. """
        def wrapper(func):
            self._add("POST", path, func)
            return func
        return wrapper


class MiniHandler(BaseHTTPRequestHandler):
    router: ClassVar[MiniRouter]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        self._handle("GET")

    def do_POST(self) -> None:
        self._handle("POST")

    def _handle(self, method: str) -> None:
        func = self.router.dispatch(method, self.path)
        if func:
            status, headers, body = func(self)
            self.send_response(status)
            for key, value in headers.items():
                self.send_header(key, value)
                self.end_headers()
                self.wfile.write(body)
        else:
            self.send_error(404, "Not found")


class Miniroute(HTTPServer):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        router: MiniRouter = MiniRouter(),
        *args,
        **kwargs
    ) -> None:
        """ Miniroute class to access the server app. """
        handler = MiniHandler
        handler.router = router
        self.router = router
        kwargs.pop("RequestHandlerClass") if "RequestHandlerClass" in kwargs.keys() else None
        args = [a for a in list(args) if not isinstance(a, BaseHTTPRequestHandler)]
        super().__init__((host, port), handler, *args, **kwargs) # pyright: ignore[reportArgumentType]

    def run(self, poll_interval: float = 0.5) -> None:
        """ this method is just running serve_forever() under another name. """
        self.serve_forever(poll_interval=poll_interval)

