import TLSSocketWrapper
import re

class CLIInterface:
    def __init__(self, server: TLSSocketWrapper.TLSSocketWrapper):
        self.server_socket = server

    def start_attempt(self, server_name):
        """Prints start and connection attempt messages."""
        print("[+] Starting CLI Interface...")
        print(f"[+] Connecting to server {server_name}...")

    def attempt_failed(self, server_name):
        """Prints a message when connection to server fails."""
        print(f"[-] Failed to connect to server {server_name}.")

    def attempt_reconnect(self, server_name):
        """Prints a message when attempting to reconnect."""
        print(f"[+] Attempting to reconnect to server {server_name}...")

    def no_more_servers(self):
        """Prints a message when no servers are available."""
        print("[-] Cannot connect to any server.")
        print("[-] Exiting...")

    def success_connect(self, server_name):
        """Prints a message when connection to server is successful."""
        print(f"[+] Connected to {server_name}.")
        print("[+] Ready to send commands.")
        print("[+] For help, type 'help'.]")

    def help(self):
        """Display available CLI commands."""
        print("[+] Available commands:")
        print("  - help: Show this help message")
        print("  - write record#<number> <bytes>: Write a <bytes> to location 00 of key17")
        print("  - read record#<number>: Read the bit string")
        print("  - exit: Exit the CLI")

    def command_attempt(self):
        """
        Prints a message indicating a command attempt.
        """
        print(f"[*] Executing command...")

    def command_success(self, response):
        """
        Prints a message indicating a successful command operation.
        """
        print(f'[*] {response}')

    def read(self, record_number):
        """
        Read a bit string from the specified record number by sending a request to the server.

        Args:
            record_number (int): The record number to read from.
        """
        print(f"[*] Reading...")
        self.server_socket.read(record_number)
        print(f'[*] {self.server_socket.receive().decode().strip()}')

    def exit(self):
        """Prints exit messages for the CLI."""
        print("[+] Closing connection to server...")
        print("[+] Exiting CLI...")

    def invalid_format(self):
        """Prints a message for invalid command format."""
        print("[-] Error: Invalid command format.")
    
    def invalid_write_args(self):
        print("[-] Error: 'write' command requires record number and bytes data")
        print("[*] Usage: write record#<number> <bytes>")

    def invalid_read_args(self):
        print("[-] Error: 'read' command requires record number")
        print("[*] Usage: read record#<number>")
    
    def invalid_record(self):
        print("[-] Error: Invalid record number format.")
        print("[*] Format: record#<number>")

    def invalid_command(self):
        print("[-] Unknown command")
