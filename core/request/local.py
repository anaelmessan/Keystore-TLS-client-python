from operator import methodcaller
from core.request.interface import BaseRequest
import threading

class LocalRequest(BaseRequest):
    """
    A class that represents a request with its response.

    Depends on:
        TLSSocketWrapper: name of the methods to use.
    """
    def __init__(self, keystore: str, method: tuple[str, ...], response_queue = None):
        self.__response = None
        self.__keystore = keystore
        self.__SocketWrapperMethodCaller = methodcaller(*method)
        self.__done = threading.Event()
        self.__error = None
        self.__simultaneous_queue = response_queue

    def get_keystore(self):
        """
        Get the request's keystore.

        Returns:
            str: keystore hostname.
        """
        return self.__keystore

    def process_request(self, socketWrapper):
        """
        Send the request, retrieve the response then stores it.

        Args:
            socketWrapper (TLSSocketWrapper): TLSSocketWrapper instance.
        """

        try:
            self.__response = self.__SocketWrapperMethodCaller(socketWrapper)
            if self.__simultaneous_queue:
                self.__simultaneous_queue.put(self)
        except Exception as e:
            self.__error = e
        finally:
            self.__done.set()


    def get_response(self, timeout=None):
        """
        Returns the response of the client (blocking).

        Argument:
            timeout (int): timeout to get a response.

        Returns:
            bytes: the response.

        Raises:
            Exceptions of socketWrapper.
        """
        self.__done.wait(timeout)
        if self.__error:
            raise self.__error
        return self.__response

