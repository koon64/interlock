import json


class APIKeys:
    def __init__(self, path=None):

        DEFAULT_PATH = 'lib/InterlockKeys.json'

        if path is None:
            path = DEFAULT_PATH

        self.path = path
        with open(path) as f:
            self.keys = json.load(f)

    def get(self, key_name):
        if key_name in self.keys:
            return self.keys[key_name]
        else:
            return False

