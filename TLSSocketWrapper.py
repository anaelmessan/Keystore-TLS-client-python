from OpenSSL import SSL, crypto
import socket

class TLSSocketWrapper:
    def __init__(self):
        self.__create_ssl_context()

    @staticmethod
    def __create_ssl_context():
        ssl_context = SSL.Context(SSL.TLS_METHOD)
        ssl_context.set_min_proto_version(SSL.TLS1_3_VERSION)
        ssl_context.set_max_proto_version(SSL.TLS1_3_VERSION)
        try:
            ssl_context.set_cipher_list(b"TLS_AES_128_CCM_SHA256")
        except Exception as e:
            print(f"Error: Could not set specific cipher suites: {e}")
        #-no_ticket
        ssl_context.set_session_cache_mode(SSL.SESS_CACHE_OFF)
        #context.set_psk_client_callback(psk_client_callback)

        return ssl_context


    def connect(self):
        pass

    def receive(self):
        pass

    def send(self,data):
        pass