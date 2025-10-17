from interface.CLI_Interface_Abstract import CLIInterface
from aws_client_utils.constants import AWS_CLIENT_RESPONSE_CODES as RESPCODE

# TODO : send the strings through the socket instead of printing them


class CLIInterfaceAWS(CLIInterface):
    # client_socket : the socket of the connected client
    def __init__(self, aws_socket):
        self.client_socket = aws_socket


    def start_attempt(self, server_name):
        pass

    def attempt_failed(self, server_name):
        # """Prints a message when connection to server fails."""
        # self.client_socket.send(
        #     f"[-] Failed to connect to server {server_name}.\n".encode("utf-8")
        # )
        pass

    def attempt_reconnect(self, server_name):
        pass

    def no_more_servers(self):
        """Prints a message when no servers are available."""
        # self.client_socket.send("[-] Cannot connect to any server.\n".encode("utf-8"))
        # self.client_socket.send("[-] Exiting...\n".encode("utf-8"))
        pass


    def success_connect(self, server_name):
        """Prints a message when connection to server is successful."""
        # self.client_socket.send(f"[+] Connected to {server_name}.\n".encode("utf-8"))
        # self.client_socket.send("[+] Ready to send commands.\n".encode("utf-8"))
        # self.client_socket.send("[+] For help, type 'help'.]\n".encode("utf-8"))
        pass

    def help(self):
        # """Display available CLI commands."""
        # self.client_socket.send("[+] Available commands:\n".encode("utf-8"))
        # self.client_socket.send("  - help: Show this help message\n".encode("utf-8"))
        # self.client_socket.send(
        #     "  - write record#<number> <bytes>: Write a <bytes> to location 00 of key17\n".encode(
        #         "utf-8"
        #     )
        # )
        # self.client_socket.send(
        #     "  - read record#<number>: Read the bit string\n".encode("utf-8")
        # )
        # self.client_socket.send("  - exit: Exit the CLI\n".encode("utf-8"))
        pass

    def command_attempt(self):
        """
        Prints a message indicating a command attempt.
        """
        # self.client_socket.send(f"[*] Executing command...\n".encode("utf-8"))
        pass

    def command_success(self, response):
        """
        Prints a message indicating a successful command operation.
        """
        if response is not 'OK':

            self.client_socket.send(bytes.fromhex('00' + response))
        else:
            pass

    def exit(self):
        """Prints exit messages for the CLI."""
        # self.client_socket.send("[+] Closing connection to server...\n".encode("utf-8"))
        # self.client_socket.send("[+] Exiting CLI...\n".encode("utf-8"))
        pass

    def invalid_format(self):
        """Prints a message for invalid command format."""
        # self.client_socket.send("[-] Error: Invalid command format.\n".encode("utf-8"))
        pass

    def invalid_write_args(self):
        # self.client_socket.send(
        #     "[-] Error: 'write' command requires record number and bytes data\n".encode(
        #         "utf-8"
        #     )
        # )
        # self.client_socket.send(
        #     "[*] Usage: write record#<number> <bytes>\n".encode("utf-8")
        # )
        pass

    def invalid_read_args(self):
        # self.client_socket.send(
        #     "[-] Error: 'read' command requires record number\n".encode("utf-8")
        # )
        # self.client_socket.send("[*] Usage: read record#<number>\n".encode("utf-8"))
        pass

    def invalid_record(self):
        # self.client_socket.send(
        #     "[-] Error: Invalid record number format.\n".encode("utf-8")
        # )
        # self.client_socket.send("[*] Format: record#<number>\n".encode("utf-8"))
        pass

    def invalid_command(self):
        # self.client_socket.send("[-] Unknown command\n".encode("utf-8"))
        pass

    def invalid_key_index(self):
        # self.client_socket.send(
        #     "[-] Error: Invalid key number format.\n".encode("utf-8")
        # )
        # self.client_socket.send(
        #     "[*] Format: key#<xy>, <xy> is the key index (00, 01, 02, 03)\n".encode(
        #         "utf-8"
        #     )
        # )
        pass

    def invalid_hexa(self):
        # self.client_socket.send(
        #     "[-] Error: Invalid AES key, must be a 32-character hexadecimal.\n".encode(
        #         "utf-8"
        #     )
        # )
        pass

    def invalid_setkey_args(self):
        # self.client_socket.send(
        #     "[-] Error: 'define' command requires key index and hexadecimal key\n".encode(
        #         "utf-8"
        #     )
        # )
        # self.client_socket.send(
        #     "[*] Usage: define key#<xy> <hex[32]>\n".encode("utf-8")
        # )
        pass

    def unexpected_error(self, error_msg):
        # self.client_socket.send("[-] Error: Unexpected Error\n".encode("utf-8"))
        # self.client_socket.send(error_msg + "\n".encode("utf-8"))
        pass

    def invalid_encrypt(self):
        # self.client_socket.send(
        #     "[-] Error: 'encrypt' command requires key index and hexadecimal data\n".encode(
        #         "utf-8"
        #     )
        # )
        # self.client_socket.send(
        #     "[*] Usage: encrypt key#<xy> <hex[32]>\n".encode("utf-8")
        # )
        pass

    def invalid_decrypt(self):
        # self.client_socket.send(
        #     "[-] Error: 'decrypt' command requires key index and hexadecimal data\n".encode(
        #         "utf-8"
        #     )
        # )
        # self.client_socket.send(
        #     "[*] Usage: decrypt key#<xy> <hex[32]>\n".encode("utf-8")
        # )
        pass
