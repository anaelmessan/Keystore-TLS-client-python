import core.tls.socket_wrapper
import socket
from core.tools.read_config import readconfig
import threading
from core.tls.hsm_connection import ConnectionWorker
from core.request.local import LocalRequest
from queue import Queue


def main():
    keystores = readconfig("config.yaml")

    for keystore_infos in keystores:
            ConnectionWorker(*keystore_infos)

    ConnectionWorker.start_all()

    try:
        # To get the response of a request (the results can only be retrieved sequencially)
        request = LocalRequest("key22.com", ("read_record", 1))
        ConnectionWorker.dispatch_request(request)
        response = request.get_response() #blocking
        print(response)

        # To get the first result of multiple concurrent requests (since get_response is blocking):
        request_queue = Queue()
        request1 = LocalRequest("key22.com", ("read_record", 1), request_queue)
        request2 = LocalRequest("key17.com", ("read_record", 1), request_queue)
        ConnectionWorker.dispatch_request(request1)
        ConnectionWorker.dispatch_request(request2)
        first = request_queue.get()

        print(first.get_response())
        print("Winner", first.get_keystore())


    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
