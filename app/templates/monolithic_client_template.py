import core.tls.socket_wrapper
import socket
from core.tools.read_config import readconfig
import threading
from core.tls.hsm_connection import ConnectionWorker
from core.request.local import LocalRequest


def main():
    keystores = readconfig("config.yaml")

    for keystore_infos in keystores:
            ConnectionWorker(*keystore_infos)

    ConnectionWorker.start_all()

    try:
        request = LocalRequest("key22.com", ("read_record", 1))
        ConnectionWorker.dispatch_request(request)
        #print(f"Encryption client request for: {request.get_keystore()}, => handled by thread : {thread_id}")
        print(request.get_response())


    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
