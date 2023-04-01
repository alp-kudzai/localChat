import socket
import sys
import threading
import time

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

# need 2 threads, 1 for user input and 1 for receiving data from server
def InputThread():
    while True:
        message = input('Enter a Message: ')
        if message == ":q":
            client_socket.close()
            break
        client_socket.sendall(message.encode())
        time.sleep(0.5)

def ReceiveMsgs():
    while True:
        try:
            data = client_socket.recv(1024)
            message = data.decode()
            # if not message:
            #     client_socket.close()
            #     break
            print(message)
        except TimeoutError:
            continue
        except OSError:
            print("exiting...")
            client_socket.close()
            sys.exit()
        
    # except:
    #     # print("\nAn Expection occured!")
    #     continue
print("Creating and running threads!")
Input_thread = threading.Thread(target=InputThread)
Receive_Msgs = threading.Thread(target=ReceiveMsgs)

Receive_Msgs.start()
#give time to make connection and get welcome message from server
time.sleep(0.5)
Input_thread.start()

# Input_thread.join()
# Receive_Msgs.join()

    