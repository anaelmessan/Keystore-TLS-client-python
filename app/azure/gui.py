from app.graphics.tinker import AppWindow
from app.azure.cloud_handler import AzureCloudHandler
from app.azure.key_provider import AzureKEKProvider


def main():

    path = "config/azure.credentials"
    key_provider = AzureKEKProvider()


    cloud = AzureCloudHandler(key_provider,path)

    win = AppWindow(cloud)
    win.run()

main()
