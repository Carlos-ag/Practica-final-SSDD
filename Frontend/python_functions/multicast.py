import socket
import struct
import threading
import time
import eel

# Placeholder for multicast IP and port
MCAST_GRP = 'localhost'
port = 1
last_written_port = 0


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
    print("Starting multicast listener")
    global last_written_port
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

        # Set a timeout for the socket to make sure it doesn't block indefinitely
        sock.settimeout(1)

        if last_written_port != current_port:
            print(f"Listening for messages on {current_grp}:{current_port}")
            last_written_port = current_port
        try:
            data, _ = sock.recvfrom(1024)  # This may timeout after 1 second
            data = data.decode('utf-8')
            print(f"Received multicast message: {data}")
            # message looks like this:
            # message = f"<USER_ID>{user_id}</USER_ID><MESSAGE>{message}</MESSAGE>"
            # TODO: FALTA
            user_id = data.split('<USER_ID>')[1].split('</USER_ID>')[0]
            message = data.split('<MESSAGE>')[1].split('</MESSAGE>')[0]
            eel.add_chat_message(user_id, message)
        except socket.timeout:
            pass  # Timeout occurred, loop will check stop_event again
        except socket.error:
            pass  # Handle other socket errors
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
