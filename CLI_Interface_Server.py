from CLI_Interface_Abstract import CLIInterface

#TODO : send the strings through the socket instead of printing them

class CLIInterfaceServer(CLIInterface):
    # client_socket : the socket of the connected client
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def start_attempt(self, server_name):
        """Prints start and connection attempt messages."""
        self.client_socket.send("[+] Starting CLI Interface...".encode("utf-8"))
        self.client_socket.send(f"[+] Connecting to server {server_name}...".encode("utf-8"))

    def attempt_failed(self, server_name):
        """Prints a message when connection to server fails."""
        self.client_socket.send(f"[-] Failed to connect to server {server_name}.".encode("utf-8"))

    def attempt_reconnect(self, server_name):
        """Prints a message when attempting to reconnect."""
        self.client_socket.send(f"[+] Attempting to reconnect to server {server_name}...".encode("utf-8"))

    def no_more_servers(self):
        """Prints a message when no servers are available."""
        self.client_socket.send("[-] Cannot connect to any server.".encode("utf-8"))
        self.client_socket.send("[-] Exiting...".encode("utf-8"))

    def success_connect(self, server_name):
        """Prints a message when connection to server is successful."""
        self.client_socket.send(f"[+] Connected to {server_name}.".encode("utf-8"))
        self.client_socket.send("[+] Ready to send commands.".encode("utf-8"))
        self.client_socket.send("[+] For help, type 'help'.]".encode("utf-8"))

    def help(self):
        """Display available CLI commands."""
        self.client_socket.send("[+] Available commands:".encode("utf-8"))
        self.client_socket.send("  - help: Show this help message".encode("utf-8"))
        self.client_socket.send("  - write record#<number> <bytes>: Write a <bytes> to location 00 of key17".encode("utf-8"))
        self.client_socket.send("  - read record#<number>: Read the bit string".encode("utf-8"))
        self.client_socket.send("  - exit: Exit the CLI".encode("utf-8"))

    def command_attempt(self):
        """
        Prints a message indicating a command attempt.
        """
        self.client_socket.send(f"[*] Executing command...".encode("utf-8"))

    def command_success(self, response):
        """
        Prints a message indicating a successful command operation.
        """
        self.client_socket.send(f'[*] {response}'.encode("utf-8"))

    def exit(self):
        """Prints exit messages for the CLI."""
        self.client_socket.send("[+] Closing connection to server...".encode("utf-8"))
        self.client_socket.send("[+] Exiting CLI...".encode("utf-8"))

    def invalid_format(self):
        """Prints a message for invalid command format."""
        self.client_socket.send("[-] Error: Invalid command format.".encode("utf-8"))
    
    def invalid_write_args(self):
        self.client_socket.send("[-] Error: 'write' command requires record number and bytes data".encode("utf-8"))
        self.client_socket.send("[*] Usage: write record#<number> <bytes>".encode("utf-8"))

    def invalid_read_args(self):
        self.client_socket.send("[-] Error: 'read' command requires record number".encode("utf-8"))
        self.client_socket.send("[*] Usage: read record#<number>".encode("utf-8"))
    
    def invalid_record(self):
        self.client_socket.send("[-] Error: Invalid record number format.".encode("utf-8"))
        self.client_socket.send("[*] Format: record#<number>".encode("utf-8"))

    def invalid_command(self):
        self.client_socket.send("[-] Unknown command".encode("utf-8"))
