import boto3
import aws_encryption_sdk
from botocore.configloader import load_config
import os


class AmazonS3CloudHandler:
    """
    Class to handle requests to the cloud.
    To keep compatibility, implement the public methods.
    """
    def __init__(self, credentials_path = None):
        self.__service_name = "AmazonS3"

        self.boto3_resource = None
        self.connected = False
        #self.key_provider = key_provider
        self.credentials_path = credentials_path

    def get_list_containers(self) -> list[str]:
        """
        Returns:
            list[string]: the list of the names of containers (or buckets).
        """
        return list(self.boto3_resource.buckets.all())

    def get_list_files(self, container_name: str) -> list[str]:
        """
        Returns:
            list[string]: the list of the names of files (or blobs) inside a container.
        """
        container = self.boto3_resource.Bucket(container_name)
        #TODO
        return []

    def connect_hsm(self):
        """
        Connects to the HSM.
        """
        self.key_provider.connect()

    def connect_cloud(self):
        """
        Connects to the cloud (if needed).
        """

        #TODO error handling
        creds_data = load_config(os.path.join(self.credentials_path, "credentials"))
        creds_default_profile = creds_data["profiles"]["default"]

        aws_access_key_id = creds_default_profile.get("aws_access_key_id")
        aws_secret_access_key = creds_default_profile.get("aws_secret_access_key")

        config_data = load_config(os.path.join(self.credentials_path, "config"))
        config_default_profile = config_data.get("default", {})

        region = config_default_profile.get("region")

        self.boto3_resource = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region
        )

        # try:
        #     print(self.boto3_client.list_buckets())
        # except Exception as e:
        #     print("Error connecting to Amazon S3")
        #     print(e)
        #     return


        # try:
        #     config = load_config(self.credentials_path)
        #
        # except Exception:
        #     print("Could not read Azure credentials. Using Azurite credentials.")
        #     connection_string = ("DefaultEndpointsProtocol=http;"
        #     "AccountName=devstoreaccount1;"
        #     "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        #     "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
        #     "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
        #     "TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;")
        self.connected = True
        print("Connected to", self.__service_name)

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
