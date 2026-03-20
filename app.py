from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def index():
    try:
        response = requests.get("http://yourname.duckdns.org:8080", timeout=5)
        return response.text
    except Exception as e:
        return f"Could not connect to server: {e}"
```
> Replace `yourname.duckdns.org` and `8080` with your actual DuckDNS domain and port

### `requirements.txt`
Create another file named `requirements.txt`:
```
flask
requests
gunicorn
