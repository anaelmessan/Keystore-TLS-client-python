from command.Command_Abstract import Command
import re


class ReadHandler(Command):
    def execute(self, cli, socket, cmdline):
        if len(cmdline) != 2:
            cli.invalid_read_args()
            return
        match = re.search(r"record#(\d+)", cmdline[1])
        if not match:
            cli.invalid_record()
            return
        record_number = int(match.group(1))
        self.read(cli, socket, record_number)

    def read(self, cli, socket, record_number):
        """
        Read a bit string from the specified record number by sending a request to the server.

        Args:
            record_number (int): The record number to read from.
        """
        cli.command_attempt()
        socket.read(record_number)
        cli.command_success(socket.receive().decode().strip())
