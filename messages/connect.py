from pickle import dumps


class MessageConnect:
    somedata = 1

    def pack(self):
        return dumps(self)
