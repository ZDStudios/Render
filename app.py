from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def index():
    try:
        response = requests.get("http://zdstudios.duckdns.org:25566", timeout=5)
        return response.text
    except Exception as e:
        return f"Could not connect to server: {e}"
