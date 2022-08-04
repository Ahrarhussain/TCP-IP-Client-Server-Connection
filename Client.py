import socket
import select
import errno    #error code...to match specific errors..when we know we can't receive the msgs
import sys

HEADER_LENGTH = 10

IP = "192.168.117.175"
PORT = 6767

my_username = input("Username: ")         #when client joins immediately
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))      #to connect
client_socket.setblocking(False)       #receive function won't be blocking


#send these infos to the server

username = my_username.encode("utf-8")
username_header= f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    #send msgs and receive msgs
    #message = input(f"{my_username} > ")
    message = ""
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
    
    try:   #accept we hit an error...we are going to hit the error at some point for sure
        while True:
            #receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the serv")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")


            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:  #when there are no more msgs to receive
            print('Reading error', str(e))
            sys.exit()
        continue
    except Exception as e:
        print('General error', str(e))
        sys.exit()