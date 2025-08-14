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
        #Cipher cannot be set
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options &= ssl.OP_NO_TICKET
        return ssl_context

    def set_psk(self,psk):
        self.__psk = psk
        self.__context.set_psk_client_callback(lambda hint: ("Client_identity", self.__psk))

    def connect(self, hostname=None, port=None):
        if hostname is None:
            hostname = self.__hostname
        if port is None:
            port = self.__port
        if not hostname or not port:
            raise Exception("Hostname or port not set")

        sock = socket.create_connection((hostname, port), timeout=10)

        try:
            print(self.__hostname)
            self.__ssock = self.__context.wrap_socket(sock, server_hostname=self.__servername)
            print(f"✅ Connected using {self.__ssock.version()}")
        except Exception as e:
            sock.close()
            raise Exception(f"TLS handshake failed: {e}")




    def receive(self):
        pass

    def send(self,data):
        pass
    def __str__(self):
        return ""