import socket
import select  #this code will run the same whether we are on Mac, WIndows or Linux

HEADER_LENGTH = 10
IP = "192.168.117.175"
PORT = 6767

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #so we don't have to change the port no again and again

server_socket.bind((IP, PORT))

server_socket.listen() 


#list of clients...for the time being in this case list of sockets

sockets_list = [server_socket]

#client dictionary: client socket the key, user data the value
clients = {}

# RECEIVE MESSAGE
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):   #when we don't get any value client closed the connection
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        return {"header":message_header, "data": client_socket.recv(message_length)}


    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)   # three parameters, sockets we might read, sockets we write on, sockets we might air on

    for notified_socket in read_sockets:
        if notified_socket == server_socket:  #someone just connected and we need to handle for it
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)   # function defined above
            if user is False: #someone disconnected
                continue
            sockets_list.append(client_socket)

            clients[client_socket] = user    #dictionary of clients

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")        #embedding inside quotes and using f string

        else: 
            message=receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user=clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket !=notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]



