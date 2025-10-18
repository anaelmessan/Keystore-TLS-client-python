from command.Command_Abstract import Command
import re


class EncryptHandler(Command):
    def execute(self, cli, socket, cmdline):
        if len(cmdline) != 3:
            cli.invalid_encrypt()
            return
        match = re.fullmatch(r"key#(\d{2})", cmdline[1])
        if not match:
            cli.invalid_key_index()
            return
        index_key = int(match.group(1))
        if index_key >= 4:
            self.CLI.invalid_key_index()
        else:
            bytes_data = cmdline[2]
            self.encrypt(cli, socket, index_key, bytes_data)

    def encrypt(self, cli, socket, index_key: str, bytes_data: str):
        valid_data = self.is_valid_hexa(cli, bytes_data)
        if valid_data:
            cli.command_attempt()
            socket.encrypt(index_key, bytes_data)
            cli.command_success(socket.receive().decode().strip())
