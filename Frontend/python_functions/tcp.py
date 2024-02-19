import python_functions.global_variables as global_variables
import socket

def read_tcp_address_from_file(file_path):
    """
    Reads the TCP server's IP and port from a given file.

    Parameters:
    - file_path: The path to the file containing address information.

    Returns:
    - A tuple containing the IP and port if found, otherwise (None, None).
    """
    try:
        with open(file_path, "r") as file:
            for line in file:
                method, ip, port = line.strip().split(',')
                if method.upper() == 'TCP':
                    return ip, int(port)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except ValueError:
        print(f"Error processing {file_path}. Check the file format.")
    
    return None, None


# create a function to connect to a tcp server
def connet_to_tcp_server(ip, port):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server
    s.connect((ip, port))
    global_variables.tcp_s = s
    print("Connected to TCP server.")

# create a function to send a message to a tcp server
def send_tcp_message(message, chat_id, user_id):

    if global_variables.tcp_s is None:
        ip, port = read_tcp_address_from_file("addresses.txt")
        if ip is not None and port is not None:
            connet_to_tcp_server(ip, port)
        else:
            print("No TCP server address found.")
            return "ERROR"
    s = global_variables.tcp_s
    # messages look like this: 
    # <CHAT_ID> chat_id_info </CHAT_ID>
    # <USER_ID> user_id_info </USER_ID>
    # <MESSAGE> message_info </MESSAGE>
    # split the message by the tags
    message = f"<CHAT_ID>{chat_id}</CHAT_ID><USER_ID>{user_id}</USER_ID><MESSAGE>{message}</MESSAGE>"
    # send the message to the server
    s.send(message.encode('utf-8'))
    print(f"Sent message to TCP server: {message}")
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
