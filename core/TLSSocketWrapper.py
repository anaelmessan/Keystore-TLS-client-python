import ssl
import socket


class TLSSocketWrapper:
    """
    TLS socket wrapper for secure client-server communication.

    Handles TLS 1.3 connection setup, PSK authentication, and
    Keystore command sending (read, write, encrypt, decrypt, etc.).
    """

    def __init__(self, servername, hostname=None, port=None):
        """
        Initialize the TLS socket wrapper and SSL context.

        Args:
            servername (str): Server Name for TLS handshake.
            hostname (str): Server IP or hostname.
            port (int): Server port.
        """

        print("Using OpenSSL ", ssl.OPENSSL_VERSION_INFO)
        self.__hostname = hostname
        self.__port = port
        self.__servername = servername
        self.__context = self.__create_ssl_context()
        self.__ssock = None
        self.__psk = None

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

    def connect(self, hostname=None, port=None):
        """
        Establish a secure TLS connection with the given server.

        Args:
            hostname (str, optional): Hostname to connect to.
            port (int, optional): Server port.
        Returns:
            TLSSocketWrapper: The active socket wrapper instance.
        Raises:
            Exception: If connection or TLS handshake fails.
        """

        if hostname is None:
            hostname = self.__hostname
        if port is None:
            port = self.__port
        if not hostname or not port:
            print("Hostname or port not set")
            raise Exception("Hostname or port not set")
        sock = socket.create_connection((hostname, port), timeout=10)

        try:
            self.__ssock = self.__context.wrap_socket(
                sock, server_hostname=self.__servername
            )

        except Exception as e:
            sock.close()
            raise Exception(f"TLS handshake failed: {e}")

        return self

    def echo(self, msg):
        """
        Send an echo command.

        Args:
            msg (str): Message to send for testing.
        """

        data = f"?01{msg}\n".encode("utf-8")
        self.__ssock.send(data)

    def read(self, record_number):
        """
        Reads the bit string stored at the specified record number (location 00 of key17).
        This method reconnects to the server for each command due to server timeout constraints.
        Sends a read command to the server for the given record number.

        Args:
            record_number (int): The record number to read from.
        """
        data = f"I{record_number:02x}\n".encode("utf-8")
        self.__ssock.send(data)

    def write(self, record_number, bytes_data):
        """
        Writes a bit string to the specified record number (location 00 of key17).
        This method reconnects to the server for each command due to server timeout constraints.
        Sends a write command to the server with the given record number and bit string.

        Args:
            record_number (int): The record number to write to.
            bytes_data (str): The bit string to write.
        """
        data = f"Z{record_number:02x}{bytes_data}\n".encode("utf-8")
        self.__ssock.send(data)

    def set_key(self, index_key, bytes_data):
        """
        Define a new AES key on the Keystore.

        Args:
            index_key (int): Key index (00–03).
            bytes_data (str): 32-character hexadecimal AES key.
        """

        data = f"t{index_key:02x}{bytes_data}\n".encode("utf-8")
        self.__ssock.send(data)

    def encrypt(self, index_key, bytes_data):
        """
        Encrypt data using the AES key at the specified index.

        Args:
            index_key (int): Key index (00–03).
            bytes_data (str): Hexadecimal data to encrypt.
        """

        data = f"A{index_key:02x}{bytes_data}\n".encode("utf-8")
        self.__ssock.send(data)

    def decrypt(self, index_key, bytes_data):
        """
        Decrypt data using the AES key at the specified index.

        Args:
            index_key (int): Key index (00–03).
            bytes_data (str): Hexadecimal data to decrypt.
        """

        data = f"a{index_key:02x}{bytes_data}\n".encode("utf-8")
        self.__ssock.send(data)

    def receive(self):
        """
        Receive raw data from the TLS socket.

        Returns:
            bytes: Data received from the server.
        """

        return self.__ssock.recv()

    def close(self):
        """
        Send a termination command and close the TLS socket.
        """

        data = "?02\n".encode("utf-8")
        self.__ssock.send(data)
        self.__ssock.close()

    def close_socket(self):
        """
        Close the TLS socket
        """

        self.__ssock.close()

    def send(self, bytes_data):
        # celle qui va gérer les trucs des ip je pense

        self.__ssock

    def __str__(self):
        return ""
