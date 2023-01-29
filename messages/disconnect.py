from pickle import dumps


class MessageDisconnect:
    somedata = 1

    def pack(self):
        return dumps(self)
