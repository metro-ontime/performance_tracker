import pendulum
from .helpers.s3_resource import S3_resource
from .helpers.fs_resource import FS_resource

datastores = {
    "S3": S3_resource,
    "filesystem": FS_resource
}

class Context:
    def __init__(self, config):
        self.config = config
        self.datastore = datastores[config["datastore"]["name"]](config["datastore"]["path"])
        self.tmp = FS_resource(config["tmp_dir"])

    def logger(self, stuff, datetime=pendulum.now()):
        print(datetime, stuff, sep=",")
