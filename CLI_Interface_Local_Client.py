from CLI_Interface_Abstract import CLIInterface


class CLIInterfaceLocalClient(CLIInterface):
    def __init__(self):
        # No attributes to initialize
        pass

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
        print("[+] For help, type 'help'.\n")

    def help(self):
        """Display available CLI commands."""
        print("[+] Available commands:")
        print("  - help: Show this help message")
        print(
            "  - write record#<number> <bytes>: Write a <bytes> to location 00 of key17"
        )
        print("  - read record#<number>: Read the bit string")
        print(
            "  - define key#<xy> <hex[32]>: Define an AES key. <xy> is the key index (00, 01, 02, 03), and <hex[32]> is a 32-character hexadecimal key."
        )
        print(
            "  - encrypt key#<xy> <hex[32]>: Encrypt the given 32-hexadecimal bytes using key index <xy>."
        )
        print(
            "  - decrypt key#<xy> <hex[32]>: Decrypt the given 32-hexadecimal bytes using key index <xy>."
        )
        print("  - exit: Exit the CLI")

    def command_attempt(self):
        """
        Prints a message indicating a command attempt.
        """
        print("[*] Executing command...")

    def command_success(self, response):
        """
        Prints a message indicating a successful command operation.
        """
        print(f"[*] {response}")

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

    def invalid_key_index(self):
        print("[-] Error: Invalid key number format.")
        print("[*] Format: key#<xy>, <xy> is the key index (00, 01, 02, 03)")

    def invalid_hexa(self):
        print("[-] Error: Invalid AES key, must be a 32-character hexadecimal.")

    def invalid_setkey_args(self):
        print("[-] Error: 'define' command requires key index and hexadecimal key")
        print("[*] Usage: define key#<xy> <hex[32]>")

    def unexpected_error(self, error_msg):
        print("[-] Error: Unexpected Error")
        print(error_msg)

    def invalid_encrypt(self):
        print("[-] Error: 'encrypt' command requires key index and hexadecimal data")
        print("[*] Usage: encrypt key#<xy> <hex[32]>")

    def invalid_decrypt(self):
        print("[-] Error: 'decrypt' command requires key index and hexadecimal data")
        print("[*] Usage: decrypt key#<xy> <hex[32]>")
