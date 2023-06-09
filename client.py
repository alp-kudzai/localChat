import socket
import sys

# define the server's IP address and port number
SERVER_HOST = '192.168.8.110'  # replace with the server's IP address
SERVER_PORT = 4444  # replace with the server's port number

# create a new socket object using the IPv4 address family and TCP protocol
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

#set a timeout so its non-blocking
client_socket.settimeout(1)

# receive the welcome message from the server
try:
    data = client_socket.recv(1024)
    message = data.decode()
    print(message)
except:
    print("Couldn't connect to server!")
    sys.exit(1)

# loop to send and receive messages
while True:
    # get input from the user
    message = input('Enter a message: ')
    
    if message == ":q":
        client_socket.close()
        break

    # send the message to the server
    client_socket.sendall(message.encode())

    # receive the response from the server
    data = client_socket.recv(1024)
    message = data.decode("utf-8")
    print(message)

print('Exited Server!')
