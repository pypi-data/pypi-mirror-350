# miniroute/miniroute.py
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, ClassVar


class MiniRouter:
    """
    Router for miniroute server.

    Args:
        routes (dict[(str, str), Callable]): A dict with a tuple of the HTTP
                method and URI that returns the associated Callable.
                ! You should not pass a routes dict but decorate your function.
    """
    def __init__(self, routes: dict[tuple[str, str], Callable] = {}) -> None:
        self.routes = routes

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


class Miniroute(ThreadingMixIn, HTTPServer):
    """
    Miniroute class that represents your HTTP server.

    Args:
        host (str): server name.
        port (int): port number.
        router (MiniRouter): MiniRouter instance.
        quiet (bool): overrides log_message to None.
        daemon_threads (bool): authorizes concurrency.
        legacy (bool): makes this object acts exactly as the HTTPServer
    """
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        router: MiniRouter = MiniRouter(),
        quiet: bool = False,
        daemon_threads: bool = False,
        legacy: bool = False,
        *args,
        **kwargs
    ) -> None:
        # HTTPServer magic here
        kwargs.pop("RequestHandlerClass", None)
        kwargs.pop("daemon_threads", None)
        self._handler = MiniHandler
        self._handler.router = router
        self._server_address = (host, port)
        args = [a for a in list(args) if not isinstance(a, BaseHTTPRequestHandler)]
        if quiet:
            self._handler.log_message = lambda *args: None # pyright: ignore
        self._args = args
        self._kwargs = kwargs
        # Attributs for ThreadingMixIn
        self.daemon_threads = daemon_threads
        # Attributes specific for miniroute internal working
        self.router = router
        self.legacy = legacy
        if self.legacy:
            self._init_http_server()

    def _init_http_server(self) -> None:
        HTTPServer.__init__(
            self,
            self._server_address,
            self._handler,
            *self._args,
            **self._kwargs
        )

    def run(self, poll_interval: float = 0.5) -> None:
        """
        serve_forever() proxy.
        Handle requests until an explicit shutdown() request.
        It also calls service_actions(),
        which may be used by a subclass or mixin to provide actions
        specific to a given service.

        args:
            poll_interval (float): Poll for shutdown every poll_interval seconds.
        """
        if not self.legacy:
            self._init_http_server()
        self.serve_forever(poll_interval=poll_interval)

