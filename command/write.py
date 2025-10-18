from command.Command_Abstract import Command
import re


class WriteHandler(Command):
    def execute(self, cli, socket, cmdline):
        if len(cmdline) != 3:
            cli.invalid_write_args()
            return
        match = re.search(r"record#(\d+)", cmdline[1])
        if not match:
            cli.invalid_record()
            return
        record_number = int(match.group(1))
        bytes_data = cmdline[2]
        self.write(cli, socket, record_number, bytes_data)

    def write(self, cli, socket, record_number, bytes_data):
        """
        Write a bit string to the specified record number by sending a request to the server.

        Args:
            record_number (int): The record number to write to.
            bytes_data (str): The bit string to write.
        """
        cli.command_attempt()
        socket.write(record_number, bytes_data)
        cli.command_success(socket.receive().decode().strip())
