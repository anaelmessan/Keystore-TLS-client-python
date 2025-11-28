from app.graphics.tinker import AppWindow
from app.google.cloud_handler import GoogleCloudHandler
from app.google.key_provider import KEKProvider


def main():
    key_provider = KEKProvider()

    cloud = GoogleCloudHandler(key_provider, fake_GCS=True)
    win = AppWindow(cloud)
    win.run()


main()
