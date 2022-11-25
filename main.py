from googledrive import GoogleDrive

driver = GoogleDrive()
file = input("Enter file path: ")
driver.upload(file)
# driver.search()
# file = input("Enter file id: ")
# driver.download(file)
