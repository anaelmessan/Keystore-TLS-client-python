import socket
import threading
import sys
from CLI_Interface_Server import CLIInterfaceServer
from Controller import Controller

HOST = "0.0.0.0"  # Listen on all interfaces
DEFAULT_PORT = 5123

# TODO:
# <...client socket initialization>
# controller = Controller.Controller(CLIInterfaceServer(client_socket))   #Put this somewhere after each distant client connection
# #Do this then :
# while True:
#     command = input("Enter command: ")  #here retrieve command from socket
#     status = controller.run_command(command)
#     if status is False:
#         break


def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    controller = Controller(CLIInterfaceServer(conn))
    with conn:
        while True:
            conn.send(b"Enter command:\n")
            command = conn.recv(1024)
            status = controller.run_command(command.decode())
            if status is False:
                break
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
