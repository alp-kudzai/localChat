import socket
import threading
import time

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.Clients = []
        #timeout 
        self.sock.settimeout(1)

    def listen(self):
        self.sock.listen(5)
        while True:
            try:
                client, address = self.sock.accept()
            except socket.timeout:
                continue
            #added another exception for Ctrl+C and close all sockets
            self.Clients.append((client, address))
            #timeout
            client.settimeout(1)
            client.sendall('Welcome to LoChat!'.encode())
            print(f"Connected to: {address[0]}, {address[1]}")
            
            threading.Thread(target = self.listenToClient,args = (client,address)).start()


    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                received_msg = data.decode()
                if not received_msg:
                    self.Clients.remove((client, address))
                    client.close()
                    print(f"Client disconnected: {address[0]}:{address[1]}")
                    return False
                elif received_msg:
                    # Set the response to echo back the recieved data 
                    response = f'\nMessage Received'.encode()
                    print(f'\nReceived: {received_msg}\nFrom: {address[0]}:{address[1]}')
                    client.sendall(response)
                    for clt in self.Clients:
                        #if clt != (client, address):
                        # if the ip are diff; or ; Ip are same and port diff
                        if (clt[1][0] != address[0]) or ((clt[1][0] == address[0]) and (clt[1][1] != address[1])):
                            clt[0].sendall(f'\nFrom {address[0]}: {received_msg}'.encode())
                            #print('sent...HELLO!')
                        #[( soc, (ip,port) )]
            except (socket.timeout, ConnectionResetError):
                #print(f'{address[0]}:{address[1]} timed out!')
                continue


if __name__ == "__main__":
    # while True:
    #     port_num = int(input("Port? "))
    #     try:
    #         port_num = int(int(port_num))
    #         break
    #     except ValueError:
    #         pass
    print(f"Starting Server on port {4444}")
    ThreadedServer('0.0.0.0',4444).listen()