from pickle import dumps


class TestData:
    test = 1

    def pack(self):
        return dumps(self)
