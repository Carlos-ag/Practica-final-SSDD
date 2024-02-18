import socket
import struct
import threading
import time
import eel

# Placeholder for multicast IP and port
MCAST_GRP = 'localhost'
port = 1


stop_event = None
listener_thread = None

# Lock for synchronizing access to multicast settings
settings_lock = threading.Lock()

def read_multicast_address():
    global MCAST_GRP
    try:
        with open("addresses.txt", "r") as file:
            for line in file:
                method, ip, _ = line.strip().split(',')
                if method.upper() == 'MULTICAST':
                    with settings_lock:
                        MCAST_GRP = ip
                    print(f"Updated multicast IP to {MCAST_GRP}")
                    break  # Found the multicast address, no need to continue reading
    except FileNotFoundError:
        print("addresses.txt not found. Using default MCAST_GRP.")
    except ValueError:
        print("Error processing addresses.txt. Using default MCAST_GRP.")

def change_multicast_listening_port(new_port):
    global port
    with settings_lock:
        port = new_port
    print(f"Updated multicast listening port to {port}")
    restart_multicast_listener()

def multicast_listener(stop_event):
    while not stop_event.is_set():
        with settings_lock:
            current_port = port
            current_grp = MCAST_GRP

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', current_port))
        
        group = socket.inet_aton(current_grp)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print(f"Listening for messages on {current_grp}:{current_port}")
        try:
            data, _ = sock.recvfrom(1024)  # This will block until a message is received
            data = data.decode('utf-8')
            eel.add_chat_message(data)
        except socket.error:
            pass  # Handle errors (e.g., timeout)
        finally:
            sock.close()

def restart_multicast_listener():
    global listener_thread, stop_event
    if listener_thread is not None:
        stop_event.set()
        listener_thread.join()

    stop_event = threading.Event()
    listener_thread = threading.Thread(target=multicast_listener, args=(stop_event,))
    listener_thread.start()

# Initial setup
def init_multicast_client():
    read_multicast_address()
    restart_multicast_listener()
