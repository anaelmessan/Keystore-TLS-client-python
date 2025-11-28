from app.graphics.tinker import AppWindow
from app.azure.cloud_handler import AzuriteCloudHandler
from app.azure.key_provider import AzureKEKProvider

def main():

    key_provider = AzureKEKProvider()


    cloud = AzuriteCloudHandler(key_provider)

    win = AppWindow(cloud)
    win.run()

main()
