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

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            self.Clients.append((client, address))
            client.sendall('Welcome to LoChat!'.encode())
            print(f"Connected to: {address[0]}, {address[1]}")
            #client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                received_msg = data.decode()
                if not received_msg:
                    client.close()
                    print(f"Client disconnected: {address[0]}:{address[1]}")
                    return False
                elif received_msg:
                    # Set the response to echo back the recieved data 
                    response = f'\nMessage Received'.encode()
                    print(f'\nReceived: {received_msg}')
                    client.sendall(response)
                    for clt in self.Clients:
                        #if clt != (client, address):
                        # if the ip are diff; or ; Ip are same and port diff
                        if (clt[1][0] != address[0]) or ((clt[1][0] == address[0]) and (clt[1][1] != address[1])):
                            clt[0].sendall(f'\nFrom {address[0]}: {received_msg}'.encode())
                            #print('sent...HELLO!')
                        #[( soc, (ip,port) )]
                
                time.sleep(0.2)
            except:
                client.close()
                return False

if __name__ == "__main__":
    # while True:
    #     port_num = int(input("Port? "))
    #     try:
    #         port_num = int(int(port_num))
    #         break
    #     except ValueError:
    #         pass
    print(f"Starting Server on port {4444}")
    ThreadedServer('0.0.0.0','4444').listen()