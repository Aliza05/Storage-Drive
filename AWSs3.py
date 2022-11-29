import boto3
import botocore
from storagedrive import StorageDrive


class AWSCloud(StorageDrive):

    s3 = boto3.resource('s3')

    def download(self, file_id):
        bucket_name = 'storagedrive18' # replace with your bucket name
        key = '3.png' # replace with your object key

        try:
            self.s3.Bucket(bucket_name).download_file(key, '3.png')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    def upload(self, file_path):
        # Upload a new file
        data = open('GM.png', 'rb')
        self.s3.Bucket('storagedrive18').put_object(Key='GM.png', Body=data)

    def search(self):
        # Print out bucket names
        for bucket in self.s3.buckets.all():
            print(bucket.name)

