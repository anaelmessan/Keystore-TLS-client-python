import server_socket
import re

class CLIInterface:
    def __init__(self, server: server_socket.server_socket):
        self.server_socket = server

    def start(self):
        server_names = ["key17", "key20"]
        server_value = 0
        print("[+] Starting CLI Interface...")
        print(f"[+] Connecting to server {server_names[server_value]}...")
        connexion = self.server_socket.connect()
        while not connexion:
            print(f"[-] Failed to connect to {server_names[server_value]}.")
            if server_value + 1 >= len(server_names):
                print("[-] No more servers to connect to.")
                print("[-] Cannot connect to any server.")
                print("[-] Exiting...")
                exit()
            server_value += 1
            print(f"[+] Attempting to connect to {server_names[server_value]}...")
            connexion = self.server_socket.connect()
        print(f"[+] Connected to {server_names[server_value]}.")
        print(connexion)
        print("[+] Ready to send commands.")
        print("[+] For help, type 'help'.]")

    def help(self):
        print("[+] Available commands:")
        print("  - help: Show this help message")
        print("  - write record#<number> <bytes>: Write a <bytes> to location 00 of key17")
        print("  - read record#<number>: Read the bit string")
        print("  - exit: Exit the CLI")

    def write(self, record_number, bytes_data):
        print(f"[+] Writing to record {record_number}: {bytes_data}")
        self.server_socket.write(record_number, bytes_data)
        print(self.server_socket.recv())

    def read(self, record_number):
        print(f"[+] Reading from record {record_number}")
        self.server_socket.read(record_number)
        print(self.server_socket.recv())

    def exit(self):
        self.server_socket.close()

    def run_command(self, command):
        parts = command.split()
        cmd = parts[0]
        if cmd == "help":
            self.help()
        elif cmd == "exit":
            self.exit()
            return False
        elif "\r\n" in command or "`" in command:
            print("[-] Error: Invalid command format.")
            return False
        elif cmd == "write":
            if len(parts) != 3:
                print("[-] Error: 'write' command requires record number and bytes data")
                print("[*] Usage: write record#<number> <bytes>")
                return
            match = re.search(r"#(\d+)", parts[1])
            if not match:
                print("[-] Error: Invalid record number format.")
                print("[*] Format: record#<number>")
                return
            record_number = int(match.group(1))
            bytes_data = parts[2]
            self.write(record_number, bytes_data)
        elif cmd == "read":
            if len(parts) != 2:
                print("[-] Error: 'read' command requires record number")
                print("[*] Usage: read record#<number>")
                return
            match = re.search(r"#(\d+)", parts[1])
            if not match:
                print("[-] Error: Invalid record number format.")
                print("[*] Format: record#<number>")
                return
            record_number = int(match.group(1))
            self.read(record_number)
        else:
            print("[-] Unknown command")
