import frontend.my_python_code.global_variables as global_variables
import socket

# create a function to connect to a tcp server
def connet_to_tcp_server(ip, port):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server
    s.connect((ip, port))
    global_variables.tcp_s = s

# create a function to send a message to a tcp server
def send_tcp_message(message, chat_id, user_id):
    if global_variables.tcp_s is None:
        connet_to_tcp_server("localhost", 12345)
    s = global_variables.tcp_s
    # messages look like this: 
    # <CHAT_ID> chat_id_info </CHAT_ID>
    # <USER_ID> user_id_info </USER_ID>
    # <MESSAGE> message_info </MESSAGE>
    # split the message by the tags
    message = f"<CHAT_ID>{chat_id}</CHAT_ID><USER_ID>{user_id}</USER_ID><MESSAGE>{message}</MESSAGE>"
    # send the message to the server
    s.send(message.encode('utf-8'))
    # wait for OK response
    response = s.recv(1024).decode('utf-8')
    return response


# create a function to receive a message from a tcp server
def receive_tcp_message(s):
    # receive the message from the server
    return s.recv(1024).decode('utf-8')

# create a function to close the connection to a tcp server
def close_tcp_connection(s):
    # close the connection
    s.close()

# create a function to send a message to a tcp server and receive a response
