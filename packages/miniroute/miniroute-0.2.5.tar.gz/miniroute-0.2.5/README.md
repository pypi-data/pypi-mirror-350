# Miniroute

**Miniroute** is a minimal HTTP framework that only uses code from on Python’s built-in `http.server`, designed for lightweight local servers and IPC tooling.

It only adds 80 lines of code while everything it rests on is 100% native from python.
This tool is meant for really basic and local http communication, preferably inter-process.
For most of these kind of jobs, the standard `http.server` module is enough, but is a **pain** to integrate, in terms of boilerplate code.


### Warning

As the officiel `http` module documentation state : **This is NOT a server to be used in PRODUCTION.**

**This module doesn't address any security flaws that `http` may bring up.**

**It's encouraged to be familiar with [http.server documentation before using miniroute](https://docs.python.org/3/library/http.server.html#http.server.HTTPServer)**

### Installation

```bash
pip install miniroute
```

### Usage

The Miniroute class inherits the `http.server.HTTPServer` class, and integrates a router by
having its own `RequestHandlerClass` which always replaces the one you would pass.
It also has a `run` method that is only a renamed `serve_forever` method.
Apart from that, it can be used exactly as you would use a `http.server.HTTPServer` object.

```python
from miniroute import Miniroute
import json

app = Miniroute(host="localhost", port=5000)

@app.router.get("/hello")
def hello(handler):
    body = json.dumps({"message": "Hello, world!"}).encode()
    headers = [("Content-Type", "application/json")]
    return 200, headers, body

@app.router.post("/echo")
def echo(handler):
    length = int(handler.headers.get("Content-Length", 0))
    data = handler.rfile.read(length)
    return 200, [("Content-Type", "application/json")], data

if __name__ == "__main__":
    app.run()
```

### Route handlers

Each route function:

- Receives the current `BaseHTTPRequestHandler` as argument
- Must return a tuple:
  `status_code: int, headers: dict[str, str], body: bytes`

Example:

```python
return 200, [("Content-Type", "text/plain")], b"OK"
```

### License

PSF License
You are free to use, modify, and distribute this software under the terms of the Python Software Foundation License.

> This project is not affiliated with or endorsed by the Python Software Foundation.

