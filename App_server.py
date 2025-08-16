import socket
import threading
import sys

HOST = "0.0.0.0"  # Listen on all interfaces
DEFAULT_PORT = 5123

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[{addr}] {data.decode(errors='ignore').strip()}")
            conn.sendall(b"Hello from multi-client Python server!\n")
    print(f"[-] Connection closed: {addr}")

def main():
    try:
        port = int(sys.argv[1])
    except Exception:
        port = DEFAULT_PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen()
        print(f"[*] Listening on {HOST}:{port}...")

        while True:
            conn, addr = s.accept()
            # Start a new thread for each client
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True  # So threads close when main program ends
            thread.start()

if __name__ == "__main__":
    main()
