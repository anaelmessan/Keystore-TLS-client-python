from google.cloud import storage
from google.auth.credentials import AnonymousCredentials
from google.api_core.exceptions import Conflict
import tink
from tink import aead, cleartext_keyset_handle
from tink.proto import aes_gcm_pb2, tink_pb2, common_pb2
import os

GCSENDPOINT = "http://localhost:4443"


class StorageService:
    def __init__(self, fake_GCS: bool = False):
        aead.register()
        self.client = self.create_client(fake_GCS)

    def create_client(self, fake_GCS):
        if fake_GCS:
            client = self.create_client_fakeGCS()
        else:
            client = self.create_client_GCS()
        return client

    def create_client_fakeGCS(self):
        client = storage.Client(
            credentials=AnonymousCredentials(),
            project="test",
            client_options={"api_endpoint": GCSENDPOINT},
        )
        print(f"Google Storage client connected to Fake GCS Server {GCSENDPOINT}")
        print(client)
        return client

    def create_client_GCS(self):
        pass

    def list_buckets(self, all_files: bool = False):
        print("[Bucket]")
        buckets = {}
        for bucket in self.client.list_buckets():
            print(f"{bucket.name}{'/' if all_files else ''}")
            buckets[bucket.name] = []
            if all_files:
                for blob in bucket.list_blobs():
                    print(f" - {blob.name}")
                    buckets[bucket.name].append(blob.name)
        return buckets

    def show_file_tree(self):
        return self.list_buckets(all_files=True)

    def create_bucket(self, bucket_name):
        try:
            bucket = self.client.create_bucket(bucket_name)
            return bucket
        except Conflict:
            return "[Info] Bucket already exists."
        except Exception as e:
            return f"[Error] Failed to create the bucket :\n {e}"

    def __ensure_bucket_exists(self, bucket_name):
        buckets = self.list_buckets()
        if bucket_name in buckets:
            return True
        else:
            user_input = input(
                "[Info] Bucket doesn't exist, do you want to create ? (yes/no)\n"
            )
            if user_input.lower() == "yes":
                self.create_bucket(bucket_name)
                return True
            else:
                return False

    def __get_tink_primitive(self, raw_key_bytes):
        gcm_key_proto = aes_gcm_pb2.AesGcmKey(version=0, key_value=raw_key_bytes)
        key_data = tink_pb2.KeyData(
            type_url="type.googleapis.com/google.crypto.tink.AesGcmKey",
            value=gcm_key_proto.SerializeToString(),
            key_material_type=tink_pb2.KeyData.SYMMETRIC,
        )
        key = tink_pb2.Keyset.Key(
            key_data=key_data,
            status=tink_pb2.ENABLED,
            key_id=1,
            output_prefix_type=tink_pb2.TINK,
        )
        keyset = tink_pb2.Keyset(primary_key_id=1, key=[key])
        handle = cleartext_keyset_handle.from_keyset(keyset)
        return handle.primitive(aead.Aead)

    def upload_file(self, bucket_name, filepath, key_bytes):
        if not os.path.exists(filepath):
            return f"[Error] File '{filepath}' not found."
        try:
            with open(filepath, "rb") as f:
                plaintext_data = f.read()

            cipher = self.__get_tink_primitive(key_bytes)
            ciphertext = cipher.encrypt(plaintext_data, b"")

            if not self.__ensure_bucket_exists(bucket_name):
                return False

            bucket = self.client.bucket(bucket_name)
            blob_name = os.path.basename(filepath)
            blob = bucket.blob(blob_name)
            if blob.exists():
                user_input = input(
                    f"[Info] File '{blob_name}' already exists in the bucket. Do you want to overwrite it? (yes/no)\n"
                )
                if user_input.lower() == "no":
                    return f"[Error] Upload has been cancelled by user. {blob_name} already exists."

            blob.metadata = {
                "encryption": "tink-aes-gcm-256-hsm",
                "ck": key_bytes.hex(),
            }
            blob.upload_from_string(ciphertext)

            return (
                f"[Success] File has been uploaded to GS : //{bucket_name}/{blob_name}"
            )

        except Exception as e:
            raise e
            return f"Erreur lors de l'upload : {str(e)}"

    def download_file(self, bucket_name, cloud_file_path, user_file_path):
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.get_blob(cloud_file_path)

            if not blob:
                return "[Error] : File not found."
            if os.path.isfile(user_file_path):
                user_input = input(
                    f"[Info] {user_file_path} already exists. Do you want to overwrite it? (yes/no)\n"
                )
                if user_input.lower() == "no":
                    return f"[Error] Upload has been cancelled by user. {user_file_path} already exists."

            encrypted_content = blob.download_as_bytes()
            print("key : ", blob.metadata["ck"])
            print("encrypted_content : ", encrypted_content)
            key = bytes.fromhex(blob.metadata["ck"])

            cipher = self.__get_tink_primitive(key)
            plaintext = cipher.decrypt(encrypted_content, b"")

            with open(user_file_path, "wb") as f:
                f.write(plaintext)
            return "[Success] File downloaded"

        except Exception as e:
            raise e
            return f"[Error] Downloading file has failed\n {e}"

    def delete_all(self):
        buckets = list(self.client.list_buckets())
        if not buckets:
            return "[Info] No buckets found."
        report = ["[Error] Cannot delete buckets:"]
        for bucket in buckets:
            try:
                blobs = list(self.client.list_blobs(bucket))
                if blobs:
                    bucket.delete_blobs(blobs)
                bucket.delete()
            except Exception as e:
                print(f"[Error] Cannot delete buckets: {bucket.name}")


# client = StorageService(fake_GCS=True)
# client.list_buckets()
# client.create_bucket("test4")
# client.show_file_tree()
# key = os.urandom(32)
# print(key)
# print(client.upload_file("test5", "test.txt", key))
# client.list_buckets()
# client.download_file("test5", "test.txt", "download.txt")
# client.delete_all()
# client.list_buckets()
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, HttpResponseError


class AzureCloudHandler:
    def __init__(self, fake_GCS: bool = False):
        aead.register()
        self.client = None
        self.connected = False
        self.fake_GCS = fake_GCS

    def connect_cloud(self, fake_GCS):
        if fake_GCS:
            client = self.create_client_fakeGCS()
        else:
            client = self.create_client_GCS()
        self.connected = True
        print("Connected")

    def create_client_fakeGCS(self):
        client = storage.Client(
            credentials=AnonymousCredentials(),
            project="test",
            client_options={"api_endpoint": GCSENDPOINT},
        )
        print(f"Google Storage client connected to Fake GCS Server {GCSENDPOINT}")
        print(client)
        return client

    def create_client_GCS(self):
        pass

    def get_list_containers(self):
        return list(self.client.list_buckets())

    def get_list_files(self, container_name: str):
        bucket = self.storage_client.bucket(container_name)
        return list(bucket.list_blobs())

    def connect_hsm(self):
        self.key_provider.connect()

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
        blob_client = self.blob_service_client.get_container_client(
            container_name
        ).get_blob_client(filename)
        blob_client.require_encryption = True
        blob_client.key_encryption_key = self.key_provider
        blob_client.encryption_version = "2.0"
        return blob_client
