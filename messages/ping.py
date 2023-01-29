from pickle import dumps


class Ping:

    def pack(self):
        return dumps(self)
