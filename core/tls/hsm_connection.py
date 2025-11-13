from core.tls.socket_wrapper import TLSSocketWrapper
import threading
import queue
import time


class ConnectionWorker:
    """
    A class that represents a connection to an HSM, with a queue of reqests to send in a thread.

    Class attribute:
        allWorkers (list): List of instances.

    Attribute:
        servername (str): Hostname of the keystore.
    """
    allWorkers = []

    def __init__(self, hostname, port, servername, psk = None, ensure_connected_before_send = True):
        self.servername = servername #ID

        # Privte
        self.__socketWrapper = TLSSocketWrapper(hostname, port, servername, psk, ensure_connected_before_send)
        self.__request_queue = queue.Queue()
        self.__worker_thread = None
        self.__running = False
        self.__lock = threading.Lock()

        ConnectionWorker.allWorkers.append(self)


    def start_worker(self):
        """
        Start a worker.
        """
        if not self.__running:
            try:
                self.__socketWrapper.connect()
                print("Connected to", self.servername)
            except Exception as e:
                print(self.__socketWrapper)
                raise e

            self.__running = True
            self.__worker_thread = threading.Thread(target=self.__process_queue, daemon=True)
            self.__worker_thread.start()

    def __process_queue(self):
        """Continuously send queued requests."""
        while self.__running:
            try:
                cmd = self.__request_queue.get(timeout=1)
            except queue.Empty:
                continue

            cmd.request_then_transmit(self.__socketWrapper)
#            except Exception as e:
#                print(e)
#                print("debug", e)
#                time.sleep(1)  # avoid spamming in case of repeated errors

    def __put_request(self, request):
        """
        Add a request to the queue of the worker.

        Args:
            request (Command): Command to add.
        """
        self.__request_queue.put(request)

    def get_socketWrapper(self):
        return self.__socketWrapper

    def is_running(self):
        """
        Check if the worker is started.

        Returns:
            True if started, else returns False.
        """
        return self.__running

    #def force_close(self):

    @classmethod
    def dispatch_request(cls, request):
        """
        Add request to the right worker's queue.

        Raises:
            LookupError
        """
        servername = request.get_keystore()
        for worker in cls.allWorkers:
            if worker.servername == servername:
                worker.__put_request(request)
                return
        raise LookupError("Keystore not found.")

    @classmethod
    def start_all(cls):
        """
        Start all workers.
        """
        for worker in cls.allWorkers:
            if not worker.is_running():
                worker.start_worker()

    @classmethod
    def stop_all(cls):
        """
        Stop all workers.
        """
        for worker in cls.allWorkers:
            if worker.is_running():
                worker.__socketWrapper.close()
                worker.__running = False

        #TODO Test
        #TODO Following :
        #@classmethod
        #persistent
        #ondemand

