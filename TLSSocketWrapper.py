from OpenSSL import SSL, crypto
import socket

class TLSSocketWrapper:
    def __init__(self, servername, hostname=None, port=None):
        self.__hostname = hostname
        self.__port = port
        self.__context = self.__create_ssl_context()
        self.__connection = self.__create_connection(self.__context, servername)

    @staticmethod
    def __create_ssl_context():
        ssl_context = SSL.Context(SSL.TLS_METHOD)
        ssl_context.set_min_proto_version(SSL.TLS1_3_VERSION)
        ssl_context.set_max_proto_version(SSL.TLS1_3_VERSION)
        # As of pyopenssl 25.1.0, no way to select the ciphersuites, only in 25.2.0
        # https://github.com/pyca/pyopenssl/pull/1432
        # try:
        #     ssl_context.set_tls13_ciphersuites(b"TLS_AES_128_CCM_SHA256")
        # except Exception as e:
        #     print(f"Error: Could not set specific cipher suites: {e}")

        #-no_ticket
        ssl_context.set_session_cache_mode(SSL.SESS_CACHE_OFF)
        #context.set_psk_client_callback(psk_client_callback)

        return ssl_context

    @staticmethod
    def __create_connection(context, servername):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        connection = SSL.Connection(context, sock)
        #-servername
        connection.set_tlsext_host_name(servername.encode())
        return connection

    def connect(self, hostname=None, port=None):
        if hostname is None:
            hostname = self.__hostname
        if port is None:
            port = self.__port
        if (hostname is None) or (port is None):
            raise Exception("Hostname or port not set")
        if self.__connection.connect_ex((hostname,port)) != 0:
            raise Exception("Error when connecting")


    def receive(self):
        pass

    def send(self,data):
        pass
    def __str__(self):
        return ""