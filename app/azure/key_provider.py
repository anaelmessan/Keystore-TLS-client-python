from core.tools.read_config import readconfig
from core.tls.hsm_connection import ConnectionWorker
from core.request.local import LocalRequest

class AzureKEKProvider:

    @staticmethod
    def wrap_key(key):
        stripped_key = key[8:]
        #TODO Manage multiple requests
        request17 = LocalRequest("key9.com", ("wrap_cek", 1, stripped_key))
        ConnectionWorker.dispatch_request(request17)
        wrapped = request17.get_response()
        return wrapped

    @staticmethod
    def unwrap_key(wrapped, algorithm):
        request17 = LocalRequest("key9.com", ("unwrap_cek", 1, wrapped))
        ConnectionWorker.dispatch_request(request17)
        stripped_key = request17.get_response()
        full_key = b"2.0\00\00\00\00\00" + stripped_key
        return full_key

    @staticmethod
    def get_key_wrap_algorithm():
        return "A256KW"
    @staticmethod
    def get_kid():
        return 1
    @staticmethod
    def connect():
        keystores = readconfig("config.yaml")
        for keystore_infos in keystores:
            ConnectionWorker(*keystore_infos)

        ConnectionWorker.start_all()
