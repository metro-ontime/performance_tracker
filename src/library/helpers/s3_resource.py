from boto3 import resource, client
import os
import json

class S3_resource:
    def __init__(self, bucket):
        self.s3 = resource("s3").Bucket(bucket)
        self.bucket_name = bucket
        self.s3_client = client("s3")

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
    
    def download(self, dest_path, source_path):
        return self.s3.Object(key=source_path).download_file(Filename=dest_path)

    def get_abs_path(self, key):
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.bucket_name,
                                                                'Key': key},
                                                        ExpiresIn=300)
        except ClientError as e:
            logging.error(e)
            return None

        return response
