from boto3 import resource

s3 = resource("s3")


def upload(filename, source_path):
    s3.Object("h4la-metro-performance", filename).upload_file(Filename=source_path)
