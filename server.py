import socket, threading, struct

HOST = "68.183.131.122" # Public IP of digital ocean droplet / use your server address
PORT = 8080
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a TCP socket to be used over ipv4
SOCKET.bind((HOST, PORT))  # Binds the ip address of server with the port number
addrbook = {"luke@gmail.com" : "Luke Skywalker", "jihoon.ryoo@sbu.edu" : "Jihoon Ryoo",
"abc@gmail.com" : "abc", "roshan.poudel@stonybrook.edu" : "Roshan Poudel"}


def handle_connections():
    """Handles different client connections"""
    SOCKET.listen()
    print(f"Server is listening on {HOST}")
    while True:  # Always keep listening
        conn, addr = SOCKET.accept()  # Accept a connection
        # After accepting a connection, handle the client connection
        # in a new thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()  # calls the handle_client method in a new thread
        print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}") # Active connections = Total threads - 1

def handle_client(conn, addr):
    """Handles each client"""
    unpacker = struct.Struct("!cb")
    header_size = struct.calcsize("!cb")
    msg_type, msg_length = unpacker.unpack(conn.recv(header_size))
    msg_type = msg_type.decode("utf-8")
    msg_length = int(msg_length)
    if msg_type != "Q" or msg_length < 0:
        send_message(conn, "Error: Unknown message protocol")
        conn.close()
        return
    email = ""
    for i in range(msg_length):
        email += conn.recv(1).decode("utf-8")
    print(f"MSG Type: {msg_type}")
    print(f"MSG Length: {msg_length}")
    print(f"MSG: {email}")
    print("MSG in dict?: ", (email in addrbook))
    if email in addrbook:
        send_message(conn, addrbook[email])
    else:
        send_message(conn, "Error: Email not found in database!")
        conn.close()

def send_message(conn, msg):
    msg_type = b"R"
    packer = struct.Struct("!cb")
    header = packer.pack(msg_type, len(msg))
    conn.send(header)
    conn.send(msg.encode("utf-8"))



handle_connections()
    
