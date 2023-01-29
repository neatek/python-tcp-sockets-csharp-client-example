# python server.py
# import pickle
from sys import getsizeof
from twisted.internet import protocol, reactor
from twisted.protocols import basic, policies
from messages.connect import MessageConnect
from messages.disconnect import MessageDisconnect
from messages.testdata import TestData

PORT = 1025
MessageDisconnectBytes = b"0DISCONNECT"
MessageConnectBytes = b"1CONNECT"
PING = b"2PING"
PONG = b"2PONG"


class MyTCPServer(protocol.Protocol, policies.TimeoutMixin):
    channels = set()
    name = ''

    def connectionMade(self):
        self.broadcast('all', MessageConnectBytes)
        self.factory.clients.append(self)
        self.name = f"#{len(self.factory.clients) - 1}"

        self.setTimeout(self.factory.timeout)
        print(f"[server] total connected: {self.get_total()}")
        # msg = MessageConnect()
        self.subscribe("all")

    def connectionLost(self, reason):
        # msg = MessageDisconnect()
        # msg.somedata = reason
        # self.unsubscribe('all')
        self.broadcast('all', MessageDisconnectBytes)
        self.factory.clients.remove(self)
        print(f"[server] total connected: {self.get_total()}")

    def dataReceived(self, data):
        # if data[:1] != b" ":
        print(f"[server] received data: <{self.name}> {data}")
        # self.transport.write(data)
        # send data to all channel
        self.broadcast("all", data)
        # self.broadcast_all(data)
        if self.name == '':
            self.name = data

        if data == PING:
            print(f"[server]: send <{PONG}> answer to {self}")
            self.transport.write(PONG)

    def broadcast_all(self, data):
        ''' Broadcast to all clients '''
        print(f"[server] broadcast data: <{getsizeof(data)}> {data}")
        for conn in self.factory.clients:
            conn.transport.write(data)

    def broadcast(self, channel, data):
        ''' Broadcast to channel '''
        count = 0
        idx = 0
        for conn in self.factory.clients:
            if channel in conn.channels:
                conn.transport.write(data)
                count += 1
            else:
                print(f"channel {channel} not found in {conn.channels}")
            idx += 1
        print(
            f"[server] broadcast data to channel <total:{count}> <{channel}>: <{getsizeof(data)}> {data}")

    def subscribe(self, channel):
        print(f"[server] client <{self}> subscribed to channel <{channel}>")
        self.channels.add(channel)

    def unsubscribe(self, channel='*'):
        if channel in self.channels:
            self.channels.remove(channel)

    def get_total(self):
        return len(self.factory.clients)


def main():
    factory = protocol.ServerFactory()
    factory.protocol = MyTCPServer
    factory.clients = []
    factory.timeout = 60
    print(f"[server] Server listening {factory}")
    reactor.listenTCP(PORT, factory)
    reactor.run()


if __name__ == "__main__":
    main()
