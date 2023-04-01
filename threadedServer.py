import socket
import threading
import time
import sys

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
        #had to make this so listen() stops looping when there are 0 clients online after they disconnect
        self.Running = True

    def listen(self):
        self.sock.listen(5)
        while self.Running:
            try:
                client, address = self.sock.accept()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                sys.exit()
            #added another exception for Ctrl+C and close all sockets
            self.Clients.append((client, address))
            #timeout
            client.settimeout(1)
            client.sendall('Welcome to LoChat!'.encode())
            print(f"Connected to: {address[0]}, {address[1]}")
            
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
        print("Exited Gracefully! Bye :)")


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
                    print(f"{len(self.Clients)} client/s online")
                    #if there are no more clients, Stop listening
                    if len(self.Clients) < 1:
                        self.Running = False
                        print(f"Running is now {self.Running}")
                    return False
                elif received_msg:
                    # respond, blue ticks (WhatsApp reference)
                    response = f'\nMessage Received'.encode()
                    print(f'\nReceived: {received_msg}\nFrom: {address[0]}:{address[1]}')
                    client.sendall(response)
                    for clt in self.Clients:
                        #if clt != (client, address): had to Tweak
                        # if the ip are diff; or ; Ip are same and port diff
                        if (clt[1][0] != address[0]) or ((clt[1][0] == address[0]) and (clt[1][1] != address[1])):
                            clt[0].sendall(f'\nFrom {address[0]}: {received_msg}'.encode())
                        #[( soc, (ip,port) )] ==> self.Clients
            except (socket.timeout, ConnectionResetError):
                #We are timing out because of the settimeout method on the sockets from both the server and client
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