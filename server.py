import socket
from _thread import *
import threading
import sys
import time



def handle_client(client_socket, client_address):
    """Handles a client connection."""
    running = True
    try:
        with client_socket:
        # send a welcome message to the client
            client_socket.sendall('Welcome to LoChat!'.encode())

            # add the client to the list of connected clients
            clients.append((client_socket, client_address))

            # loop to receive and forward messages from the client
            while running:
                #time.sleep(0.2)

                # receive a message from the client
                data = client_socket.recv(1024)
                message = data.decode()

                # if the message is empty, the client has disconnected
                if not message:
                    print(f"Closing Connection {client_address}")
                    running = False
                    break

                print(f'Received message: {message}')
                response = 'Message received'
                client_socket.sendall(response.encode())

                # iterate through the list of connected clients and send the message
                # to all clients except the client that sent the message
                for client in clients:
                    if client != (client_socket, client_address):
                        client[0].sendall(f'{client_address[0]}: {message}'.encode())
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("Function Keyboard Interrupt!")
    finally:
        # remove the client from the list of connected clients
        clients.remove((client_socket, client_address))
        # close the client socket
        client_socket.close()
  

# define the server's IP address and port number
SERVER_HOST = '0.0.0.0'  # listen on all available network interfaces
SERVER_PORT = 4444  # arbitrary port number ;)
try:
    # create a new socket object using the IPv4 address family and TCP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # bind the socket to the server's IP address and port number
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        # listen for incoming client connections
        server_socket.listen(5)

        # list to keep track of connected clients and their corresponding sockets
        clients = []

        # loop to accept incoming client connections
        while True:
            # accept a new client connection
            client_socket, client_address = server_socket.accept()

             # lock acquired by client
            # print_lock.acquire()
            print(f"Connected To: {client_address[0]}, {client_address[1]}")

            #handle_client(client_socket, client_address)

            # create a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            client_thread.join()
except KeyboardInterrupt:
    print("Outside Keyboard Interrupt!")
    sys.exit(1)
finally:
    # close the client socket
    client_socket.close()
