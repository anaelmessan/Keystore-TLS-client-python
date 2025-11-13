from operator import methodcaller

class Request:
    """
    A class that represents a request with its response and origin.

    Depends on:
        TLSSocketWrapper: name of the methods to use.

    Notes:
        Just use get_keystore() and request_then_transmit(socketWrapper).
        Close the thread and socket on exceptions.
    """
    def __init__(self, socket, request):
        self.__response = None
        self.__origin_socket = socket #some wrapper with a queue
        self.__raw_request = request
        self.__keystore = None
        self.__SocketWrapperMethodCaller = None
        self.__decode_request()

    def get_keystore(self):
        """
        Get the request's keystore.

        Returns:
            str: keystore hostname.
        """
        return self.__keystore

    def request_then_transmit(self, socketWrapper):
        """
        Send the request, retrieve the response then transmits it.

        Args:
            socketWrapper (TLSSocketWrapper): TLSSocketWrapper instance.
        """
        self.runSocketWrapperMethod(socketWrapper)
        self.send_response()



    def runSocketWrapperMethod(self, socketWrapper):
        """
        Execute the method of a TLSSocketWrapper stored in self.__SocketWrapperMethodCaller.
        Stores the response.

        Args:
            socketWrapper (TLSSocketWrapper): TLSSocketWrapper instance.

        Raises:
            Exceptions from TLSSocketWrapper.
        """
        self.__response = self.__SocketWrapperMethodCaller(socketWrapper)

    def send_response(self):
        """
        Send the stored response to the origin.

        Raises:
            TypeError: Unexpected type of the response, implement its handling.
            Exceptions related to the origin socket.
        """
        response = self.__response
        # String
        if isinstance(response, str):
            response = response.encode('utf-8')
        # Bytes-like object
        elif isinstance(response, (bytes, bytearray)):
             pass
        else:
            raise TypeError("Unexpected type for response.")

        # Add a try block or use a response dispatcher if there is concurrency on the socket (more than 1 destination per origin socket)
        self.__origin_socket.send(response)


    def __decode_request(self):
        """
        Decode the raw binary request stored in the instance.

        Raises:
            ValueError: Unknown request in the raw request.
        """

        # The cmd_id (first byte)
        cmd_id = self.__raw_request[0]

        # The cmd_id defines the format of the request
        # Here is the byte syntax of the clients' requests
        dispatch = {
            #Read record
            0 : lambda: methodcaller("read_record",self.__raw_request[2]),
                #[byte 0: 0x00 (cmd_id 0)]
                #[byte 1: keyx.com]
                #[byte 2: record number]

            #Generate Ck from k
            1 : lambda: methodcaller("other request not implemented yet"),
                #[byte 0: 0x01 (cmd_id 1)]
                #[byte 1: keyx.com]
                #[byte 0x02: key slot number]
                #[bytes 3-34: key k (256 bits)]
            }


        if cmd_id not in dispatch:
            raise ValueError(f"Unknown request ID: {cmd_id:#02x}")

        self.__SocketWrapperMethodCaller = dispatch[cmd_id]()
        self.__keystore = f"key{self.__raw_request[1]}.com"

    def set_response(self, response):
        # Set the response (unused)
        self.__response = response

