from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, HttpResponseError


class AzuriteCloudHandler:
    """
    Class to handle requests to the cloud.
    To keep compatibility, implement the public methods.
    """
    def __init__(self, key_provider):
        self.__service_name = "Azurite"
        self.__connection_string = ("DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
    "TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;")
        self.blob_service_client = None
        self.connected = False
        self.key_provider = key_provider

    def get_list_containers(self) -> list[str]:
        """
        Returns:
            list[string]: the list of the names of containers (or buckets).
        """
        # TODO error handling
        return list(self.blob_service_client.list_containers())

    def get_list_files(self, container_name: str) -> list[str]:
        """
        Returns:
            list[string]: the list of the names of files (or blobs) inside a container.
        """
        container = self.blob_service_client.get_container_client(container_name)
        return list(container.list_blobs())

    def connect_hsm(self):
        """
        Connects to the HSM.
        """
        self.key_provider.connect()

    def connect_cloud(self):
        """
        Connects to the cloud (if needed).
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(self.__connection_string)
        self.connected = True
        print("Connected")

    def upload(self, path: str, container_name: str, filename: str):
        """
        Encrypt then upload a file on the cloud.

        Arguments:
            path (str): the path of the file to upload.
            container_name (str): the name of the container to upload it to.
            filename (str): the name of the file on the cloud.
        """
        blob_client = self.__init_encryption_blob(container_name, filename)
        with open(path, "rb") as stream:
            blob_client.upload_blob(stream, overwrite=True)

    def download(self, path: str, container_name: str, filename: str):
        """
        Decrypt then download a file from the cloud.

        Arguments:
            path (str): the path of the file on the computer.
            container_name (str): the name of the container to download it from.
            filename (str): the name of the file in the container.
        """
        blob_client = self.__init_encryption_blob(container_name, filename)
        with open(path, "wb") as file:
            data = blob_client.download_blob()
            file.write(data.readall())

    def create_container(self, container_name: str):
        """
        Argument:
            container_name (str): the name of the container (or bucket) to create.
        """
        try:
            self.blob_service_client.create_container(name=container_name)
        except ResourceExistsError:
            print('A container with this name already exists.')

    def get_service_name(self):
        return self.__service_name


    def __init_encryption_blob(self, container_name, filename):
        blob_client = self.blob_service_client.get_container_client(container_name).get_blob_client(filename)
        blob_client.require_encryption = True
        blob_client.key_encryption_key = self.key_provider
        blob_client.encryption_version = '2.0'
        return blob_client
