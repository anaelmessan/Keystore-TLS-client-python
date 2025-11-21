from operator import methodcaller
from core.request.interface import BaseRequest
import threading

class LocalRequest(BaseRequest):
    """
    A class that represents a request with its response.

    Depends on:
        TLSSocketWrapper: name of the methods to use.
    """
    def __init__(self, keystore: str, method: tuple[str, ...]):
        self.__response = None
        self.__keystore = keystore
        self.__SocketWrapperMethodCaller = methodcaller(*method)
        self.__done = threading.Event()
        self.__error = None

    def get_keystore(self):
        """
        Get the request's keystore.

        Returns:
            str: keystore hostname.
        """
        return self.__keystore

    def process_request(self, socketWrapper):
        """
        Send the request, retrieve the response then transmits it.

        Args:
            socketWrapper (TLSSocketWrapper): TLSSocketWrapper instance.
        """

        try:
            self.__response = self.__SocketWrapperMethodCaller(socketWrapper)
        except Exception as e:
            self.__error = e
        finally:
            self.__done.set()

    def get_response(self, timeout=None):
        """
        """
        self.__done.wait(timeout)
        if self.__error:
            raise self.__error
        return self.__response




    #
    # def __decode_request(self):
    #     """
    #     Decode the raw binary request stored in the instance.
    #
    #     Raises:
    #         ValueError: Unknown request in the raw request.
    #     """
    #
    #     # The cmd_id (first byte)
    #     cmd_id = self.__raw_request[0]
    #
    #     # The cmd_id defines the format of the request
    #     # Here is the byte syntax of the clients' requests
    #     dispatch = {
    #         # Read record
    #         0 : lambda: methodcaller("read_record",self.__raw_request[2]),
    #             #[byte 0: 0x00 (cmd_id 0)]
    #             #[byte 1: keyx.com]
    #             #[byte 2: record number]
    #
    #         # Encrypt AES (binary)
    #         1 : lambda: methodcaller("encrypt_AES_binary", self.__raw_request[2], self.__raw_request[3:]),
    #             #[byte 0: 0x01 (cmd_id 1)]
    #             #[byte 1: keyx.com]
    #             #[byte 2: key slot number]
    #             #[bytes 3-: data blocks (up to 16 blocks)]
    #
    #         # Decrypt AES (binary)
    #         2 : lambda: methodcaller("decrypt_AES_binary", self.__raw_request[2], self.__raw_request[3:]),
    #             #[byte 0: 0x02 (cmd_id 2)]
    #             #[byte 1: keyx.com]
    #             #[byte 2: key slot number]
    #             #[bytes 3-: data blocks (up to 16 blocks)]
    #
    #         #Generate Ck from k
    #         9 : lambda: methodcaller("other request not implemented yet"),
    #             #[byte 0: 0x09 (cmd_id 9)]
    #             #[byte 1: keyx.com]
    #             #[byte 0x02: key slot number]
    #             #[bytes 3-34: key k (256 bits)]
    #         }
    #
    #
    #     if cmd_id not in dispatch:
    #         raise ValueError(f"Unknown request ID: {cmd_id:#02x}")
    #
    #     self.__SocketWrapperMethodCaller = dispatch[cmd_id]()
    #     self.__keystore = f"key{self.__raw_request[1]}.com"
    #
