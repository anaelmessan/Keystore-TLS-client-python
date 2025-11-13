# client_threads.py
import socket
import threading

HOST = "127.0.0.1"
PORT = 6123
TIMEOUT = 5.0  # secondes

def worker(name: str, payload: bytes):
    try:
        with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as s:
            print(f"[{name}] connecté à {HOST}:{PORT}")
            s.sendall(payload)
            print(f"[{name}] envoyé: {payload!r}")

            # attendre la réponse (lecture unique jusqu'à 4096 octets)
            s.settimeout(TIMEOUT)
            resp = s.recv(4096)
            if resp:
                print(f"[{name}] reçu: {resp!r}")
            else:
                print(f"[{name}] aucune donnée reçue (connexion fermée côté serveur)")
    except Exception as e:
        print(f"[{name}] erreur: {e}")

def main():
    # exemples de payloads (octets)
    payload1 = b"\x00\x11\x01"
    payload2 = b"\x00\x16\x01"

    t1 = threading.Thread(target=worker, args=("conn1", payload1))
    t2 = threading.Thread(target=worker, args=("conn2", payload2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("Terminé.")

if __name__ == "__main__":
    main()
