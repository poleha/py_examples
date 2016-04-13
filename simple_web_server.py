import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Сетевой потоковый сокет
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Настройки сокета SOL_SOCKET - тип настроек,
# SO_REUSEADDR - если сокет занят, а приходит следующий запрос - использовать заново, закрывая занятый
listen_socket.bind((HOST, PORT)) #bind socket to host and port
listen_socket.listen(1) #number specifies the number of unaccepted connections that the system will allow before
# refusing new connections
print('Serving HTTP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024) #Receive data from the socket
    print(request.decode('utf-8'))

    http_response = """
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(bytes(http_response, 'utf-8'))
    client_connection.close()
