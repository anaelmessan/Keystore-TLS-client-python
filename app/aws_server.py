import core.tls.socket_wrapper
import socket
from core.tools.read_config import readconfig
import threading
from core.tls.hsm_connection import ConnectionWorker
from core.request import Request

HOST = "0.0.0.0"  # Listen on all interfaces
DEFAULT_PORT = 6123


def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")


    with conn:
        while True:
            thread_id = threading.get_ident()
            buffer = conn.recv(1024)

            if not buffer:
                break

            try:
                request = Request(conn,buffer)
                ConnectionWorker.dispatch_request(request)
                print(f"Encryption client request for: {request.get_keystore()}, => handled by thread : {thread_id}")


            except Exception as e:
                print(e)



            #     status = controller.run_request(
            #         transcode_request(request, sock)
            #     )
            #     if not status:
            #         controller.run_request("exit")
            #         break
            # except Exception:
            #     break

    print(f"[-] Connection closed: {addr}")


def main():
    keystores = readconfig("config.yaml")

    for keystore_infos in keystores:
            ConnectionWorker(*keystore_infos)

    ConnectionWorker.start_all()


    try:
        port = int(sys.argv[1])
    except Exception:
        port = DEFAULT_PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen()
        print(f"[*] Listening on {HOST}:{port}...")

        while True:
            conn, addr = s.accept()
            # Start a new thread for each client
            thread = threading.Thread(target=handle_client, args=(conn, addr, ))
            thread.daemon = True  # So threads close when main program ends
            thread.start()


if __name__ == "__main__":
    main()
