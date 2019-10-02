import pendulum
import os
from .helpers.s3_resource import S3_resource
from .helpers.fs_resource import FS_resource

datastores = {
    "S3": S3_resource,
    "filesystem": FS_resource
}

evKeys = [
    "LOCAL_DATA",
    "DATASTORE_NAME",
    "DATASTORE_PATH",
    "TMP_DIR",
    "METRO_LINES",
    "METRO_AGENCY",
    "TIMEZONE",
    "SCHEDULE_URL",
    "VEHICLE_API_URL",
    "LOG_TIMESTAMPS"
]

class Context:
    def __init__(self):
        self.config = {}

        for k in evKeys: 
           self.config[k]=os.environ[k]
        
        self.config["METRO_LINES"] = [int(line) for line in self.config["METRO_LINES"].split(",")]
        self.datastore = datastores[self.config["DATASTORE_NAME"]](self.config["DATASTORE_PATH"])
        self.tmp = FS_resource(self.config["TMP_DIR"])
        
    def logger(self, stuff, datetime=pendulum.now('UTC')):
        if self.config["LOG_TIMESTAMPS"] == "TRUE":
            print(datetime, stuff, sep=",")
        else:
            print(stuff)
