import os
import json

class FS_resource:
    def __init__(self, path):
        self.base_dir = path

    def read(self, path):
        full_path = os.path.join(self.base_dir, path)
        with open(full_path, 'r') as infile:
            try:
                return json.load()
            except:
                return infile.read()

    def write(self, path, data):
        full_path = os.path.join(self.base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w+') as outfile:
            try:
                return json.dump(data, outfile)
            except:
                return outfile.write(data)
