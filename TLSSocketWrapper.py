import ssl
import socket


class TLSSocketWrapper:
    def __init__(self, servername, hostname=None, port=None):
        print("Using OpenSSL ", ssl.OPENSSL_VERSION_INFO)
        self.__hostname = hostname
        self.__port = port
        self.__servername = servername
        self.__context = self.__create_ssl_context()
        self.__ssock = None
        self.__psk = None

    @staticmethod
    def __create_ssl_context():
        # Cipher cannot be set
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options &= ssl.OP_NO_TICKET
        return ssl_context

    def set_psk(self, psk):
        self.__psk = psk
        self.__context.set_psk_client_callback(
            lambda hint: ("Client_identity", self.__psk)
        )

    def connect(self, hostname=None, port=None):
        if hostname is None:
            hostname = self.__hostname
        if port is None:
            port = self.__port
        if not hostname or not port:
            print("Hostname or port not set")
            raise Exception("Hostname or port not set")
        sock = socket.create_connection((hostname, port), timeout=10)

        success = False
        try:
            print(self.__hostname)
            self.__ssock = self.__context.wrap_socket(
                sock, server_hostname=self.__servername
            )
            print(f"✅ Connected using {self.__ssock.version()}")

        except Exception as e:
            sock.close()
            print(f"❌ Connection failed: {e}")
            raise Exception(f"TLS handshake failed: {e}")

        # TODO
        return self

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
        data = f"t{index_key:02x}{bytes_data}\n".encode("utf-8")
        # print(data)
        self.__ssock.send(data)

    def encrypt(self, index_key, bytes_data):
        data = f"A{index_key:02x}{bytes_data}\n".encode("utf-8")
        # print(data)
        self.__ssock.send(data)

    def decrypt(self, index_key, bytes_data):
        data = f"a{index_key:02x}{bytes_data}\n".encode("utf-8")
        # print(data)
        self.__ssock.send(data)

    def receive(self):
        return self.__ssock.recv()

    def close(self):
        data = "?02\n".encode("utf-8")
        self.__ssock.send(data)
        return False

    def __str__(self):
        return ""
