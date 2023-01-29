# Example of TCP Server/Python and C# client

This is a simple (experimental) implementation of creating a TCP socket server in Python using the Twisted library. The server implements a connection with PING/PONG, and channels to which clients can subscribe.

The connection to this server is written in Python as well as C# for completeness. Also in implementation maintenance of connection, and timeout is written.

This implementation is necessary for understanding how sockets work, and for **learning**. There are no TCP sockets in the browser, they are in nodejs, there are only Websockets in the browser.

### How to launch this:

1) Create `env` for Python project: `python3 -m venv env`
2) Activate enviroment: `./env/bin/activate`
3) Install all for requirement: `pip install -r requirements.txt`
4) Launch TCP server: `python server.py`
5) Start `csharp.exe` a few times.
6) Let's get fun with chatting


#### Links:

1. https://twisted.org
2. https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/sockets/tcp-classes
