from library import Json


class Database(dict):
    def __init__(self, pathfile="", *v, **kv):
        self.pathfile = pathfile
        super().__init__(Json.loadWrite(pathfile=pathfile))

    def save(self):
        Json.write(pathfile=self.pathfile, default=self)
