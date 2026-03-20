from flask import Flask
import socket

app = Flask(__name__)

MINECRAFT_HOST = "zdstudios.duckdns.org"
MINECRAFT_PORT = 25566

@app.route("/")
def index():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((MINECRAFT_HOST, MINECRAFT_PORT))
        sock.close()
        if result == 0:
            return f"✅ Minecraft server is ONLINE at {MINECRAFT_HOST}:{MINECRAFT_PORT}"
        else:
            return f"❌ Minecraft server is OFFLINE or unreachable"
    except Exception as e:
        return f"Error: {e}"
