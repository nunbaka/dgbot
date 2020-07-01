from library import Json


class Database(dict):
    def __init__(self, pathfile="", default={}, *v, **kv):
        self.pathfile = pathfile
        super().__init__(Json.loadWrite(pathfile=pathfile, default=default))

    def save(self):
        Json.write(pathfile=self.pathfile, default=self, sort_keys=True)
