from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, HttpResponseError


class AzureCloudHandler:
    def __init__(self, key_provider):
        self.__connection_string = ("DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
    "TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;")
        self.blob_service_client = None
        self.connected = False
        self.key_provider = key_provider

    def get_list_containers(self):
        # TODO error handling
        return list(self.blob_service_client.list_containers())

    def get_list_files(self, container_name: str):
        container = self.blob_service_client.get_container_client(container_name)
        return list(container.list_blobs())

    def connect_hsm(self):
        self.key_provider.connect()

    def connect_cloud(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(self.__connection_string)
        self.connected = True
        print("Connected")

    def upload(self, path, container_name, filename):
        blob_client = self.__init_encryption_blob(container_name, filename)
        with open(path, "rb") as stream:
            blob_client.upload_blob(stream, overwrite=True)

    def download(self, path, container_name, filename):
        blob_client = self.__init_encryption_blob(container_name, filename)
        with open(path, "wb") as file:
            data = blob_client.download_blob()
            file.write(data.readall())

    def __init_encryption_blob(self, container_name, filename):
        blob_client = self.blob_service_client.get_container_client(container_name).get_blob_client(filename)
        blob_client.require_encryption = True
        blob_client.key_encryption_key = self.key_provider
        blob_client.encryption_version = '2.0'
        return blob_client
