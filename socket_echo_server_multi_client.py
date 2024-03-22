# multiconn-server

import socket
import selectors

selection = selectors.DefaultSelector()

def accept(sock, mask):
    connection, address = sock.accept()
    print('connection from', address)
    connection.setblocking(False)
    read_func = create_read_func(address)
    selection.register(connection, selectors.EVENT_READ, read_func)

def create_read_func(address):
    def read(connection, mask):
        data = connection.recv(16)
        if data:
            print('received: ', data.decode())
            print('sending data back to the client')
            connection.sendall(data)
        else:
            print('closing connection to', address)
            selection.unregister(connection)
            connection.close()
    return read

# Multi-Binding the socket to the port
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 14344)
lsock.bind(server_address)
lsock.listen()
print('listening on {} port {}'.format(*server_address))
lsock.setblocking(False)
selection.register(lsock, selectors.EVENT_READ, accept)

# Main loop
while True:
    events = selection.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)