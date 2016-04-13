import selectors
import socket
import asyncio
asyncio.start_server

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        http_response = "Hello, World!"
        conn.sendall(bytes(http_response, 'utf-8'))
        sel.unregister(conn)
        conn.close()
        print('closing', conn)

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 8888))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

@asyncio.coroutine
def worker():
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            loop.run_in_executor(None, callback, key.fileobj, mask)

loop = asyncio.get_event_loop()
asyncio.async(worker())
loop.run_forever()