# https://github.com/hunterloftis/cryo
# https://github.com/sciyoshi/pickle-js
import pickle
from sys import getsizeof
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import protocol, reactor
from messages.testdata import TestData

PORT = 1025
PING = b"2PING"
PONG = b"2PONG"


class TCPClient(protocol.Protocol):

    def connectionMade(self):
        # data = pickle.dumps(TestData)
        data = PING
        print(f"[client] send data: {getsizeof(data)} <{data}>")
        self.transport.write(data)

    def dataReceived(self, data):
        print(f"[client] received: {data}")
        # self.transport.loseConnection()
        if data == PONG:
            print(f"[client] received PONG command")

    def connectionLost(self, reason):
        print("[client] connection lost")


class TCPFactory(ReconnectingClientFactory):
    protocol = TCPClient

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)


def main():
    f = TCPFactory()
    reactor.connectTCP("localhost", PORT, f)
    reactor.run()


if __name__ == "__main__":
    main()
