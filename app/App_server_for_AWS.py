import socket
import threading
import sys
from interface.CLI_Interface_AWS_Client import CLIInterfaceAWS
from core.Controller import Controller

HOST = "0.0.0.0"  # Listen on all interfaces
DEFAULT_PORT = 6123

# TODO:
# <...client socket initialization>
# controller = Controller.Controller(CLIInterfaceServer(client_socket))   #Put this somewhere after each distant client connection
# #Do this then :
# while True:
#     command = input("Enter command: ")  #here retrieve command from socket
#     status = controller.run_command(command)
#     if status is False:
#         break


def transcode_command(command):
    plaintext = ""
    match command[0]:
        case 0x00:
            plaintext += "read record#" + str(command[2])
    print("plaintext :", plaintext)
    return plaintext


def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    controller = Controller(CLIInterfaceAWS(conn), auto=False)
    with conn:
        while True:
            thread_id = threading.get_ident()
            command = conn.recv(1024)
            print(f"Received Bytes: {command}, => thread : {thread_id}")
            if not command:
                break
            try:
                status = controller.run_command(
                    transcode_command(command), str(command[1])
                )
                if not status:
                    break
            except Exception:
                break

    print(f"[-] Connection closed: {addr}")


def main():
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
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True  # So threads close when main program ends
            thread.start()


if __name__ == "__main__":
    main()
