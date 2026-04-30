import os
import requests
from flask import Flask, request, Response

TARGET = "http://zdstudios.duckdns.org:10531"
app = Flask(__name__)

@app.route("/", defaults={"path": ""}, methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS"])
@app.route("/<path:path>", methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS"])
def proxy(path):
    url = f"{TARGET}/{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k.lower() != "host"},
        data=request.get_data(),
        params=request.args,
        stream=True,
        timeout=120,
    )
    return Response(resp.iter_content(chunk_size=4096),
                    status=resp.status_code,
                    headers=dict(resp.headers))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
