import json

from ..miniroute import Miniroute


app = Miniroute(host="localhost", port=2683)

@app.router.get("/")
def index(handler):
    data = {'hello': 'world'}
    payload = json.dumps(data).encode("utf-8")
    headers = {"Content-Type" : "application/json"}
    return 200, headers, payload

def run():
    app.run()

