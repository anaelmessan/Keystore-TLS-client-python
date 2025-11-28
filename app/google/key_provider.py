from core.tools.read_config import readconfig
from core.tls.hsm_connection import ConnectionWorker
from core.request.local import LocalRequest


class KEKProvider:
    @staticmethod
    def wrap_key(key):
        request17 = LocalRequest("key17.com", ("wrap_cek", 1, key))
        ConnectionWorker.dispatch_request(request17)
        wrapped = request17.get_response()
        return wrapped

    @staticmethod
    def unwrap_key(wrapped):
        request17 = LocalRequest("key17.com", ("unwrap_cek", 1, wrapped))
        ConnectionWorker.dispatch_request(request17)
        stripped_key = request17.get_response()
        full_key = stripped_key
        return full_key

    @staticmethod
    def connect():
        keystores = readconfig("config.yaml")
        for keystore_infos in keystores:
            ConnectionWorker(*keystore_infos)

        ConnectionWorker.start_all()
