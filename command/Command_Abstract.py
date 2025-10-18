from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    def is_valid_hexa(self, cli, hexa: str) -> bool:
        if not hexa:
            cli.invalid_hexa()
            return False
        try:
            int(hexa, 16)
            if len(hexa) == 32:
                return True
            else:
                cli.invalid_hexa()
                return False
        except Exception:
            cli.invalid_hexa()
            return False
