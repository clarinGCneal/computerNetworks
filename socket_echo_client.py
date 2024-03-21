import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 14344)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    while True:  # Keep asking for user input
        # Send data
        message = input("Enter a message (or 'exit' to quit): ")  # Get user input
        if message == 'exit':
            break  # Exit the loop if the user types 'exit'
        print('sending: ', message)
        sock.sendall(message.encode())
        
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received: ', data.decode())
finally:
    print('closing socket')
    sock.close()