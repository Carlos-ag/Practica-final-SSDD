import socket
import threading
from chat_storage import add_message_to_chat

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

            # add_message_to_chat(chat_id, user_id, message)
            add_message_to_chat(message_info["chat_id"], message_info["user_id"], message_info["message"])

            response = "OK"
            client_socket.send(response.encode('utf-8'))
            
            # TODO: FALTA
            # send the message to the other users in the chat via multicast
            # send_message_to_chat_members_via_multicast(message_info["chat_id"], message_info["user_id"], message_info["message"])

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def start_server_tcp(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()


def create_tcp_app():
    start_server_tcp()
    print("TCP server started")