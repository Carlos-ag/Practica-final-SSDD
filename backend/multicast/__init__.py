import socket
import struct

# Initially define a default multicast IP address
MCAST_GRP = 'localhost'

try:
    with open("addresses.txt", "r") as file:
        for line in file:
            method, ip, port = line.strip().split(',')
            if method.upper() == 'MULTICAST':
                MCAST_GRP = ip
                break  # Found the multicast address, no need to continue reading
except FileNotFoundError:
    print("addresses.txt not found. Using default MCAST_GRP.")
except ValueError:
    print("Error processing addresses.txt. Using default MCAST_GRP.")

def send_multicast_message(message, port, user_id, username):
    """
    Sends a multicast message to a specified port.

    Parameters:
    - message: The message to be sent as a string.
    - port: The port number to send the message to.
    """
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set the time-to-live for messages to 1 so they do not go past the local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        message = f"<USER_ID>{user_id}</USER_ID><USERNAME>{username}</USERNAME><MESSAGE>{message}</MESSAGE>"
        # Send the message
        sock.sendto(message.encode(), (MCAST_GRP, port))
    except Exception as e:
        print(f"Error sending multicast message: {e}")
    finally:
        # Close the socket
        sock.close()
