from boto3 import resource
import os
import json

class S3_resource:
    def __init__(self, bucket):
        self.s3 = resource("s3").Bucket(bucket)
        self.bucket_name = bucket

    def read(self, path):
        return self.s3.Object(key=path).get()['Body'].read().decode('utf-8')

    def load_json(self, path):
        return json.loads(self.read(path))

    def write_json(self, path, data):
        string = json.dumps(data)
        return self.write(path, string)

    def write(self, path, data):
        return self.s3.Object(key=path).put(Body=data)

    def upload(self, dest_path, source_path):
        self.s3.Object(key=dest_path).upload_file(Filename=source_path)
        return True

    def get_abs_path(self, key):
        location = boto3.client('s3').get_bucket_location(Bucket=self.bucket_name)['LocationConstraint']
        return f"https://s3-{location}.amazonaws.com/{self.bucket_name}/{key}"
