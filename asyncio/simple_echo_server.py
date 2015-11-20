import asyncio

loop = asyncio.get_event_loop()

# an instance of EchoProtocol will be created for each client connection.
class EchoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.write(data)

    def connection_lost(self, exc):
        server.close()

# run the coroutine to establish the server connection, then keep running
# the event loop until the server is stopped.
server = loop.run_until_complete(loop.create_server(EchoProtocol, '127.0.0.1', 4444))
loop.run_until_complete(server.wait_closed())

"""
Simple echo server
This is a simple echo server, used for showing you how to start a server with a given protocol.
You can connect to it with telnet 127.0.0.1 4444. Everything you type into the telnet session will
 be sent back to you from the server.
"""