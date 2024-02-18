import socket
import struct
import eel

multicast_ip = "localhost"
port = 5007  

def multicast_client():
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # Allow multiple sockets to use the same PORT number
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to the port that we know will receive multicast data
    sock.bind(('', port))
    
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_ip)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    print(f"Listening for messages on {multicast_ip}:{port}")
    try:
        while True:
            # Receive the message and display it
            data, _ = sock.recvfrom(1024)
            data = data.decode('utf-8')
            eel.add_chat_message(data)


    except KeyboardInterrupt:
        print("Exiting multicast client")
    finally:
        # Close the socket
        sock.close()

