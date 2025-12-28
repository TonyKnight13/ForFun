from json import JSONEncoder

class mangaJsonEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__