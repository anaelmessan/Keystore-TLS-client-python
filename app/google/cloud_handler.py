from google.cloud import storage
from google.auth.credentials import AnonymousCredentials
from google.api_core.exceptions import Conflict
import tink
from tink import aead, cleartext_keyset_handle
from tink.proto import aes_gcm_pb2, tink_pb2, common_pb2
import os

GCSENDPOINT = "http://localhost:4443"


class GoogleCloudHandler:
    def __init__(self, key_provider, fake_GCS: bool = False):
        aead.register()
        self.client = None
        self.connected = False
        self.fake_GCS = fake_GCS
        self.key_provider = key_provider
        self.__service_name = ""

    def connect_cloud(self):
        print(self.fake_GCS)
        if self.fake_GCS:
            self.client = self.create_client_fakeGCS()
            self.__service_name = "Fake Google Storage"
        else:
            self.client = self.create_client_GCS()
            self.__service_name = "Google Storage"
        self.connected = True
        print("Connected")

    def create_client_fakeGCS(self):
        client = storage.Client(
            credentials=AnonymousCredentials(),
            project="test",
            client_options={"api_endpoint": GCSENDPOINT},
        )
        print(f"Google Storage client connected to Fake GCS Server {GCSENDPOINT}")
        return client

    def create_client_GCS(self):
        pass

    def get_service_name(self):
        return self.__service_name

    def get_list_containers(self):
        return list(self.client.list_buckets())

    def get_list_files(self, container_name: str):
        bucket = self.client.bucket(container_name)
        return list(bucket.list_blobs())

    def connect_hsm(self):
        self.key_provider.connect()

    def create_container(self, bucket_name):
        try:
            bucket = self.client.create_bucket(bucket_name)
            return bucket
        except Conflict:
            print("[Info] Bucket already exists.")
        except Exception as e:
            raise Exception(f"[Error] Failed to create the bucket :\n {e}")

    def upload(self, path, container_name, filename):
        with open(path, "rb") as f:
            plaintext_data = f.read()
        key_bytes = os.urandom(32)
        cipher = self.__get_tink_primitive(key_bytes)
        ciphertext = cipher.encrypt(plaintext_data, b"")
        ck = self.key_provider.wrap_key(key_bytes)
        bucket = self.client.bucket(container_name)
        blob = bucket.blob(filename)
        blob.metadata = {
            "encryption": "tink-aes-gcm-256-hsm",
            "ck": ck.hex(),
        }
        blob.upload_from_string(ciphertext)

    def download(self, path, container_name, filename):
        bucket = self.client.bucket(container_name)
        blob = bucket.get_blob(filename)
        encrypted_content = blob.download_as_bytes()
        ck = bytes.fromhex(blob.metadata["ck"])
        key = self.key_provider.unwrap_key(ck)
        cipher = self.__get_tink_primitive(key)
        plaintext = cipher.decrypt(encrypted_content, b"")
        with open(path, "wb") as f:
            f.write(plaintext)

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
