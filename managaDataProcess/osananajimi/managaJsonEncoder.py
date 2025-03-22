from json import JSONEncoder

class ManagaJsonEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__