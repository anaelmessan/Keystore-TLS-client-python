import ssl
import socket

class TLSConnectionClosed(Exception):
    """Raised when the TLS connection is closed by the server."""
    pass
class TLSReconnectFailed(Exception):
    pass
class CommandUnexpectedResponse(Exception):
    pass
class CommandErrorResponse(Exception):
    pass

class TLSSocketWrapper:
    """
    TLS socket wrapper for secure client-server communication.

    Handles TLS 1.3 connection setup, PSK authentication, and
    Keystore command sending (read, write, encrypt, decrypt, etc.).
    """

    def __init__(self, hostname, port, servername, psk = None, ensure_connected_before_send = True):
        """
        Initialize the TLS socket wrapper and SSL context.

        Args:
            servername (str): Server Name for TLS handshake.
            hostname (str): Server IP or hostname.
            port (int): Server port.
            psk (bytes): The pre-shared key value.
            ensure_connected_before_send (bool): Tries to reconnect before sending if the connection timed out

        Infos:
            30s after executing a command the server will disconnect upon the reception of another command (except for echo)
        """

        self.__hostname = hostname
        self.__port = port
        self.__servername = servername
        self.__context = self.__create_ssl_context()
        self.__ssock = None
        self.__psk = psk
        self.__ensure_connected_before_send = ensure_connected_before_send
        if psk is not None :
            self.__context.set_psk_client_callback(
            lambda hint: ("Client_identity", self.__psk)
        )

############## Read-only instance attributes ###############
    @property
    def hostname(self):
        return self.__hostname

    @property
    def servername(self):
        return self.__servername




    @staticmethod
    def __create_ssl_context():
        """
        Create and configure the TLS 1.3 context.
        """

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options &= ssl.OP_NO_TICKET
        return ssl_context

    #DEPRECATED
    def set_psk(self, psk):
        """
        Configure the Pre-Shared Key (PSK) used for TLS authentication.

        Args:
            psk (bytes): The pre-shared key value.
        """

        self.__psk = psk
        self.__context.set_psk_client_callback(
            lambda hint: ("Client_identity", self.__psk)
        )

    def connect(self):
        """
        Establish a secure TLS connection with the given server.
        Returns:
            TLSSocketWrapper: The active socket wrapper instance.
        Raises:
            Exception: If connection or TLS handshake fails.
        """
        if not self.__hostname or not self.__port:
            print("Hostname or port not set")
            raise Exception("Hostname or port not set")
        sock = socket.create_connection((self.__hostname, self.__port), timeout=10)

        try:
            self.__ssock = self.__context.wrap_socket(
                sock, server_hostname=self.__servername
            )

        except Exception as e:
            sock.close()
            raise Exception(f"TLS handshake failed: {e}")

        return self

    # def ensure_connected(self):
    #     """
    #     Ensure the socket stays connected. Use this before performing an action on the socket, possibly between 2 commands.
    #     """
    #     try:
    #         data = self.echo("test")
    #         if not data.startswith("test"):
    #             self._close_socket()
    #             self.connect()
    #     except Exception as e:
    #         print("Error: the keystore ", self.__servername, " might be busy")
    #         print(e)
    #         exit()


########## METHODS TO USE THE SOCKET ################

    def echo(self, msg):
        """
        Send an echo command.

        Args:
            msg (str): Message to send for testing.
        """

        data = f"?01{msg}\n"
        if not self.send_command(data).startswith(msg):
            raise CommandUnexpectedResponse("Echo failed")


    def read_record(self, record_number):
        """
        Reads the string stored at the specified record number.
        Sends a read command to the server for the given record number.
        Args:
            record_number (int): The record number to read from.

        Returns:
            str: The data contained in the record.
        """
        data = f"I{record_number:02x}\n"
        response = self.send_command(data)
        if response.startswith('ERROR'):
            raise CommandErrorResponse(f"Read record n°{record_number:02x} failed")
        return response

    def write_record(self, record_number, text_data):
        """
        Writes a bit string to the specified record number (location 00 of key17).
        This method reconnects to the server for each command due to server timeout constraints.
        Sends a write command to the server with the given record number and bit string.

        Args:
            record_number (int): The record number to write to.
            text_data (str): The string to write.
        """
        data = f"Z{record_number:02x}{text_data}\n"
        response = self.send_command(data)
        if not response.startswith('OK'):
            if response.startswith('ERROR'):
                raise CommandErrorResponse(f"Write record n°{record_number:02x} failed")
            else:
                raise CommandUnexpectedResponse(f"Unexpected response from server: {response}")


    def set_AES_key(self, index_key, text_data):
        """
        Define a new AES key on the Keystore.

        Args:
            index_key (int): Key index (00–03).
            bytes_data (str): 32-character hexadecimal AES key.
        """

        data = f"t{index_key:02x}{text_data}\n"
        response = self.send_command(data)
        if not response.startswith('OK'):
            if response.startswith('ERROR'):
                raise CommandErrorResponse(f"Set key n°{index_key:02x} failed")
            else:
                raise CommandUnexpectedResponse(f"Unexpected response from server: {response}")

    def encrypt_AES(self, index_key, text_data):
        """
        Encrypt data using the AES key at the specified index.

        Args:
            index_key (int): Key index (00–03).
            text_data (str): Hexadecimal data to encrypt.
        """

        data = f"A{index_key:02x}{text_data}\n"
        response = self.send_command(data)
        if response.startswith('ERROR'):
            raise CommandErrorResponse(f"Encrypting using AES key n°{index_key:02x} failed")
        return response

    def encrypt_AES_binary(self, index_key, bytes_data):
        """
        Encrypt data using the AES key at the specified index.

        Args:
            index_key (int): Key index (00–03).
            bytes_data (bytes-like object): Hexadecimal data to encrypt.
        """

        if (len(bytes_data)%16 != 0) or (len(bytes_data) == 0):
            raise ValueError("Invalid length: " + str(len(bytes_data)))

        data = f"?D{index_key:1X}".encode("utf-8") + bytes_data + "\n".encode("utf-8")
        try:
            response = self.send_command(data)
        except TLSConnectionClosed as e:
            raise CommandErrorResponse("Encryption failed.")
        return response

    def decrypt_AES_binary(self, index_key, bytes_data):
        """
        Encrypt data using the AES key at the specified index.

        Args:
            index_key (int): Key index (00–03).
            bytes_data (bytes-like object): Hexadecimal data to encrypt.
        """

        if (len(bytes_data)%16 != 0) or (len(bytes_data) == 0):
            raise ValueError("Invalid length: " + str(len(bytes_data)))

        data = f"?D{index_key+8:1X}".encode("utf-8") + bytes_data + "\n".encode("utf-8")
        try:
            response = self.send_command(data)
        except TLSConnectionClosed as e:
            raise CommandErrorResponse("Decryption failed.")
        return response




    def decrypt_AES(self, index_key, text_data):
        """
        Decrypt data using the AES key at the specified index.

        Args:
            index_key (int): Key index (00–03).
            bytes_data (str): Hexadecimal data to decrypt.
        """

        data = f"a{index_key:02x}{text_data}\n"
        response = self.send_command(data)
        if response.startswith('ERROR'):
            raise CommandErrorResponse(f"Decrypting using AES key n°{index_key:02x} failed")
        return response

    def close(self):
        """
        Send a termination command and close the TLS socket.
        """

        data = "?02\n".encode("utf-8")
        self.__ssock.send(data)
        self.__ssock.close()

    def _close_socket(self):
        """
        Close the TLS socket
        """

        self.__ssock.close()










    def receive_command_bytes(self):
        """
        Receive raw data from the TLS socket.

        Returns:
            bytes: Data received from the server.
        """
        data = self.__ssock.recv(4096)
        if data == b"":
            raise TLSConnectionClosed("Server closed connection (EOF).")
        return data

    def send_command(self,data):
        """
        Send raw data from the TLS socket.

        Returns:
            bytes or str: Data received from the server.
        Raises:
            TLSConnectionClosed: if the server closed the connection and auto-reconnect is disabled.
            TLSReconnectFailed: if reconnection or resend fails.
        """

        if isinstance(data, str):
            bytes_data = data.encode('utf-8')
            decode_output = True

        elif isinstance(data, (bytes, bytearray)):
            bytes_data = data
            decode_output = False
        else:
            raise TypeError("Wrong type")

        #TODO add a try block to ensure connection (no close socket in the except)
        self.__ssock.send(bytes_data)
        try:
            response = self.receive_command_bytes()

        except TLSConnectionClosed:
            if self.__ensure_connected_before_send:
                print("Info: reconnecting before sending data")
                try:
                    self._close_socket()
                    self.connect()
                    self.__ssock.send(bytes_data)
                    response = self.receive_command_bytes()
                except Exception as e:
                    raise TLSReconnectFailed(f"Reconnection to {self.__servername} failed: {e}") from e
                #print("Warning: auto reconnecting the socket upon server timeout which is monopolizing resources")
            else:
                raise TLSConnectionClosed("Server closed the connection (auto-reconnect disabled).")

        if decode_output:
            return response.decode()
        else:
            return response

    def __str__(self):
        return self.__hostname + str(self.__port) + str(self.__servername) + str(self.__context) + str(self.__ssock) + str(self.__psk)
