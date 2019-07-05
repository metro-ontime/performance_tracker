from helpers.s3_resource import S3_resource
from helpers.fs_resource import FS_resource
import pendulum

class Context:
    def __init__(self, config):
        self.config = config
        if config["datastore"]["name"] == "S3":
            self.datastore = S3_resource(config["datastore"]["path"])
        elif config["datastore"]["name"] == "filesystem":
            self.datastore = FS_resource(config["datastore"]["path"])

    def logger(self, stuff, datetime=pendulum.now()):
        print(datetime, stuff)
