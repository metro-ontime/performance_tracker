import os
import json

class FS_resource:
    def __init__(self, path):
        self.base_dir = path

    def read(self, path):
        full_path = os.path.join(self.base_dir, path)
        with open(full_path, 'r') as infile:
            return infile.read()

    def load_json(self, path):
        return json.loads(self.read(path))

    def write_json(self, path, data):
        string = json.dumps(data)
        return self.write(path, string)

    def write(self, path, data):
        full_path = os.path.join(self.base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w+') as outfile:
                return outfile.write(data)

    def get_abs_path(self, path):
        return os.path.join(self.base_dir, path)
