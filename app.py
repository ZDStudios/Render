import socket
import threading
import os

# Target host to forward traffic to
TARGET_HOST = "zdstudios.duckdns.org"
TARGET_PORT = 10531

# Render injects PORT via environment variable
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = int(os.environ.get("PORT", 10531))


def forward(source, destination):
    """Read from source and write to destination until connection closes."""
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    except Exception:
        pass
    finally:
        source.close()
        destination.close()


def handle_client(client_sock):
    """Open a connection to the target and bridge the two sockets."""
    try:
        target_sock = socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=10)
    except Exception as e:
        print(f"[!] Could not connect to target: {e}")
        client_sock.close()
        return

    print(f"[+] Bridging client -> {TARGET_HOST}:{TARGET_PORT}")

    # Two threads: one for each direction
    t1 = threading.Thread(target=forward, args=(client_sock, target_sock), daemon=True)
    t2 = threading.Thread(target=forward, args=(target_sock, client_sock), daemon=True)
    t1.start()
    t2.start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen(50)
    print(f"[*] Listening on {LISTEN_HOST}:{LISTEN_PORT}")
    print(f"[*] Forwarding to {TARGET_HOST}:{TARGET_PORT}")

    while True:
        client_sock, addr = server.accept()
        print(f"[+] Connection from {addr[0]}:{addr[1]}")
        t = threading.Thread(target=handle_client, args=(client_sock,), daemon=True)
        t.start()


if __name__ == "__main__":
    main()
