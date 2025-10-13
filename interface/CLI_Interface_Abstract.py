from abc import ABC, abstractmethod


class CLIInterface(ABC):
    @abstractmethod
    def start_attempt(self, server_name):
        pass

    @abstractmethod
    def attempt_failed(self, server_name):
        pass

    @abstractmethod
    def attempt_reconnect(self, server_name):
        pass

    @abstractmethod
    def no_more_servers(self):
        pass

    @abstractmethod
    def success_connect(self, server_name):
        pass

    @abstractmethod
    def help(self):
        pass

    @abstractmethod
    def command_attempt(self):
        pass

    @abstractmethod
    def command_success(self, response):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def invalid_format(self):
        pass

    @abstractmethod
    def invalid_write_args(self):
        pass

    @abstractmethod
    def invalid_read_args(self):
        pass

    @abstractmethod
    def invalid_record(self):
        pass

    @abstractmethod
    def invalid_command(self):
        pass

    @abstractmethod
    def invalid_key_index(self):
        pass

    @abstractmethod
    def invalid_hexa(self):
        pass

    @abstractmethod
    def invalid_setkey_args(self):
        pass

    @abstractmethod
    def unexpected_error(self):
        pass

    @abstractmethod
    def invalid_encrypt(self):
        pass

    @abstractmethod
    def invalid_decrypt(self):
        pass
