from core.TLSSocketWrapper import TLSSocketWrapper
import core.ReadConfig as ReadConfig
import re, time


class Controller:
    def __init__(self, cli):
        self.CLI = cli
        self.servernames = ReadConfig.dotenv_read_servernames()
        self.indexvalue = 0
        self.server_socket = ""
        self.attempt_connect()

    def run_server(self, servername):
        """
        Connect to the given server using TLS with config values.
        Returns True if successful, else False.
        """
        # Read configuration values
        host = ReadConfig.dotenv_read_host()
        port = ReadConfig.dotenv_read_port()
        psk = ReadConfig.dotenv_read_psk()
        # Initialize the TLS socket wrapper
        self.server_socket = TLSSocketWrapper(servername, host, port)
        self.server_socket.set_psk(psk)
        try:
            self.server_socket.connect()
            return True
        except Exception:
            return False

    def attempt_connect(self):
        """
        Initialize the CLI, connect to available servers, and prepare for user commands.
        Tries to connect to each server in order until successful or all fail.
        """
        servername = self.servernames[self.indexvalue]
        self.CLI.start_attempt(servername)
        attempt = self.run_server(servername)
        while attempt is False:
            self.CLI.attempt_failed(servername)
            self.indexvalue += 1
            if self.indexvalue < len(self.servernames):
                servername = self.servernames[self.indexvalue]
                self.CLI.attempt_reconnect(servername)
                attempt = self.run_server(servername)
            else:
                self.CLI.no_more_servers()
                exit()
        self.CLI.success_connect(servername)
        self.server_socket.close()

    def help(self):
        self.CLI.help()

    def write(self, record_number, bytes_data):
        """
        Write a bit string to the specified record number by sending a request to the server.

        Args:
            record_number (int): The record number to write to.
            bytes_data (str): The bit string to write.
        """
        self.CLI.command_attempt()
        self.server_socket.write(record_number, bytes_data)
        self.CLI.command_success(self.server_socket.receive().decode().strip())

    def read(self, record_number):
        """
        Read a bit string from the specified record number by sending a request to the server.

        Args:
            record_number (int): The record number to read from.
        """
        self.CLI.command_attempt()
        self.server_socket.read(record_number)
        self.CLI.command_success(self.server_socket.receive().decode().strip())

    def is_valid_hexa(self, hexa: str) -> bool:
        if not hexa:
            self.CLI.invalid_hexa()
            return False
        try:
            int(hexa, 16)
            if len(hexa) == 32:
                return True
            else:
                self.CLI.invalid_hexa()
                return False
        except Exception:
            self.CLI.invalid_hexa()
            return False

    def set_key(self, index_key: str, bytes_data: str):
        valid_data = self.is_valid_hexa(bytes_data)
        if valid_data:
            self.CLI.command_attempt()
            self.server_socket.set_key(index_key, bytes_data)
            self.CLI.command_success(self.server_socket.receive().decode().strip())

    def encrypt(self, index_key: str, bytes_data: str):
        valid_data = self.is_valid_hexa(bytes_data)
        if valid_data:
            self.CLI.command_attempt()
            self.server_socket.encrypt(index_key, bytes_data)
            self.CLI.command_success(self.server_socket.receive().decode().strip())

    def decrypt(self, index_key: str, bytes_data: str):
        valid_data = self.is_valid_hexa(bytes_data)
        if valid_data:
            self.CLI.command_attempt()
            self.server_socket.decrypt(index_key, bytes_data)
            self.CLI.command_success(self.server_socket.receive().decode().strip())

    def exit(self):
        """Close the server socket and exit the CLI."""
        # self.server_socket.close()
        self.CLI.exit()

    def run_command(self, command):
        """
        Parse and execute a CLI command by sending the appropriate request to the server.

        Args:
            command (str): The command string entered by the user.
        Returns:
            bool or None: False if the command is 'exit', otherwise None.
        """
        if not command:
            self.CLI.invalid_format()
            return False
        parts = command.split()
        cmd = parts[0]
        if cmd == "help":
            self.help()
        elif cmd == "exit":
            self.exit()
            return False
        elif "\r\n" in command or "`" in command:
            self.CLI.invalid_format()
            return False
        else:
            self.server_socket.connect()
            if cmd == "write":
                if len(parts) != 3:
                    self.CLI.invalid_write_args()
                    return
                match = re.search(r"#(\d+)", parts[1])
                if not match:
                    self.CLI.invalid_record()
                    return
                record_number = int(match.group(1))
                bytes_data = parts[2]
                self.write(record_number, bytes_data)
            elif cmd == "read":
                if len(parts) != 2:
                    self.CLI.invalid_read_args()
                    return
                match = re.search(r"#(\d+)", parts[1])
                if not match:
                    self.CLI.invalid_record()
                    return
                record_number = int(match.group(1))
                self.read(record_number)
            elif cmd == "define":
                if len(parts) != 3:
                    self.CLI.invalid_setkey_args()
                    return
                match = re.search(r"key#(\d{2})", parts[1])
                if not match:
                    self.CLI.invalid_key_index()
                    return
                index_key = int(match.group(1))
                if index_key >= 4:
                    self.CLI.invalid_key_index()
                else:
                    bytes_data = parts[2]
                    self.set_key(index_key, bytes_data)
            elif cmd == "encrypt":
                if len(parts) != 3:
                    self.CLI.invalid_encrypt()
                    return
                match = re.search(r"key#(\d{2})", parts[1])
                if not match:
                    self.CLI.invalid_key_index()
                    return
                index_key = int(match.group(1))
                if index_key >= 4:
                    self.CLI.invalid_key_index()
                else:
                    bytes_data = parts[2]
                    self.encrypt(index_key, bytes_data)
            elif cmd == "decrypt":
                if len(parts) != 3:
                    self.CLI.invalid_decrypt()
                    return
                match = re.fullmatch(r"key#(\d{2})", parts[1])
                if not match:
                    self.CLI.invalid_key_index()
                    return
                index_key = int(match.group(1))
                if index_key >= 4:
                    self.CLI.invalid_key_index()
                else:
                    bytes_data = parts[2]
                    self.decrypt(index_key, bytes_data)
            else:
                self.CLI.invalid_command()
