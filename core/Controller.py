from core.TLSSocketWrapper import TLSSocketWrapper
import core.ReadConfig as ReadConfig
from command import *


class Controller:
    """
    Main controller class for managing CLI interactions and TLS server communication.
    """

    def __init__(self, cli, auto=True):
        self.CLI = cli
        self.active_servername = ""
        self.servernames = ReadConfig.dotenv_read_servernames()
        self.indexvalue = 0
        self.server_socket = ""
        if auto:
            self.attempt_connect()  # connexion auto

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
        if servername == "key17.com" or servername == "key22.com":
            print(host)
            host = "185.216.10.85"
            print(host)
        self.server_socket = TLSSocketWrapper(servername, host, port)
        self.server_socket.set_psk(psk)
        try:
            self.server_socket.connect()
            self.active_servername = servername
            return True
        except Exception:
            self.CLI.attempt_failed(servername)
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
            self.indexvalue += 1
            if self.indexvalue < len(self.servernames):
                servername = self.servernames[self.indexvalue]
                self.CLI.attempt_reconnect(servername)
                attempt = self.run_server(servername)
            else:
                self.CLI.no_more_servers()
                exit()
        self.CLI.success_connect(servername)

    def is_socket_connected(self):
        """
        Checks if the socket is connected and reconnects if necessary.
        """
        try:
            self.server_socket.echo("is_alive")
            data = self.server_socket.receive().decode()
            if data == "":
                self.server_socket.close_socket()
                self.server_socket.connect()
        except Exception as e:
            print(e)
            exit()

    def help(self):
        """
        Displays the CLI help message.
        """
        self.CLI.help()

    def exit(self):
        """Close the server socket and exit the CLI."""
        self.server_socket.close()
        self.CLI.exit()

    def run_command(self, command, servername=None):
        """
        Parse and execute a CLI command.

        Validates the command format, ensures an active TLS connection,
        and dispatches the request to the appropriate handler or local command.

        Args:
            command (str): The command string entered by the user.
            servername (str, optional): The server to connect.
        Returns:
            bool or None: False if the command is 'exit', otherwise None.
        """
        if not command:
            self.CLI.invalid_format()
            return False
        elif "\r\n" in command or "`" in command:
            self.CLI.invalid_format()
            return False
        if self.server_socket == "":
            servername = f"key{servername}.com"
            if self.run_server(servername):
                print("serveur active: ", self.active_servername)
            else:
                return False
        else:
            self.is_socket_connected()
        cmdhandler = {
            "define": SetKeyHandler(),
            "decrypt": DecryptHandler(),
            "encrypt": EncryptHandler(),
            "write": WriteHandler(),
            "read": ReadHandler(),
        }

        local_commands = {
            "help": lambda: self.help(),
            "exit": lambda: self.exit() or False,
        }

        parts = command.split()
        cmd = parts[0].lower()  # a gerer dans les expression regulière le lower
        handler = cmdhandler.get(cmd)
        if not handler:
            if cmd in local_commands:
                result = local_commands[cmd]()
                return result if result is not None else True
            else:
                self.CLI.invalid_command()
        else:
            handler.execute(self.CLI, self.server_socket, parts)
