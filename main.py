from googledrive import GoogleDrive
from AWSs3 import AWSCloud

# driver = GoogleDrive()
# file = input("Enter file path: ")
# driver.upload(file)
# driver.search()
# file = input("Enter file id: ")
# driver.download(file)

aws = AWSCloud()
aws.search()

