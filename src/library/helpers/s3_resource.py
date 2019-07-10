from boto3 import resource
import json

class S3_resource:
    def __init__(self, bucket):
        self.s3 = resource("s3").Bucket(bucket)

    def read(self, path):
        return self.s3.Object(key=path).get()['Body'].read().decode('utf-8')

    def write(self, path, data):
        try:
            string = json.dumps(data)
        except:
            string = data
        return self.s3.Object(key=path).put(Body=string)

    def upload_file(self, filename, source_path):
        return self.s3.Object(key=filename).upload_file(Filename=source_path)
