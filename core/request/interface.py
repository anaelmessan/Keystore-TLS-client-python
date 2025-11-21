from abc import ABC, abstractmethod

class BaseRequest(ABC):
    """
    A class that represents a request with its response and origin.

    Depends on:
        TLSSocketWrapper: name of the methods to use.
    """

    @abstractmethod
    def get_keystore(self) -> str:
        """
        Get the request's keystore.

        Returns:
            str: keystore hostname.
        """
        ...

    @abstractmethod
    def process_request(self, socketWrapper):
        """
        Send the request.
        It can : store the response, signal the response is ready, or send the response.

        Args:
            socketWrapper (TLSSocketWrapper): TLSSocketWrapper instance.

        Raises:
            Exceptions from TLSSocketWrapper.
        """
        ...

