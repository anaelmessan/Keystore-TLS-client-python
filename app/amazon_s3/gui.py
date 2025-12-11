from app.graphics.tinker import AppWindow
from app.amazon_s3.cloud_handler import AmazonS3CloudHandler


def main():

    path = "config/amazon_s3"


    cloud = AmazonS3CloudHandler(path)

    win = AppWindow(cloud)
    win.run()

main()
