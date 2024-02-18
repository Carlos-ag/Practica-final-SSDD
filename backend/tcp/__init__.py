import socket
import threading
from chat_storage import save_message_to_db
from multicast import send_multicast_message

def decode_message(message):
    message_info = {
        "chat_id": None,
        "user_id": None,
        "message": None
    }
    # messages look like this: 
    # <CHAT_ID> chat_id_info </CHAT_ID>
    # <USER_ID> user_id_info </USER_ID>
    # <MESSAGE> message_info </MESSAGE>
    # split the message by the tags

    # get the chat_id
    chat_id = message.split("</CHAT_ID>")[0].split("<CHAT_ID>")[1]
    message_info["chat_id"] = chat_id

    # get the user_id
    user_id = message.split("</USER_ID>")[0].split("<USER_ID>")[1]
    message_info["user_id"] = user_id

    # get the message
    message = message.split("</MESSAGE>")[0].split("<MESSAGE>")[1]
    message_info["message"] = message

    return message_info


def handle_client(client_socket, client_address):
    try:
        print(f"Connection from {client_address} has been established.")
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Connection from {client_address} has been closed.")
                break
                
            # the message contains the CHAT_ID, the user_id and the message
            # decode the message 
            message_info = decode_message(message)
            print(f"Received message: {message_info}")

            chat_id = message_info["chat_id"]
            user_id = message_info["user_id"]
            message = message_info["message"]


            # add_message_to_chat(chat_id, user_id, message)

            save_message_to_db(chat_id, user_id, message)
            send_multicast_message(message, chat_id)

            response = "OK"
            client_socket.send(response.encode('utf-8'))
            
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def start_server_tcp(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server TCP listening on {host}:{port}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()



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

def create_tcp_app():
    """
    Initializes the TCP server using the IP and port specified in 'addresses.txt'.
    """
    ip, port = read_tcp_address_from_file("addresses.txt")
    if ip is not None and port is not None:
        start_server_tcp(ip, port)
    else:
        print("Failed to start TCP server due to missing or invalid configuration.")

