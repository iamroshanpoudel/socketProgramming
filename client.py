import socket, sys, struct

HOST = "68.183.131.122"  # Public IP Address of Digital Ocean droplet / Server running server.py
PORT = 8080
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a TCP socket to be used over ipv4

def create_socket(): 
    try:
        SOCKET.connect((HOST, PORT))  # Connects to the server via socket
    except Exception as e:
        print(f"{e} -- Check server connection")
        sys.exit(1)

def send_message():

    email = input("Enter an email to search for in the database: ").encode("utf-8")
    email_length = len(email)
    msg_type = b"Q"
    packer = struct.Struct("!cb")
    header = packer.pack(msg_type, email_length)
    SOCKET.send(header)  # header contains info about msg type and email length
    SOCKET.send(email)
    receive_response(email.decode("utf-8"))

def receive_response(email):
    unpacker = struct.Struct("!cb")
    header_size = struct.calcsize("!cb")
    msg_type, msg_length = unpacker.unpack(SOCKET.recv(header_size))
    msg_type = msg_type.decode("utf-8")
    msg_length = int(msg_length)
    if msg_type != "R" or msg_length < 0:
        print("Error: Server sent message using unknown protcol")
        SOCKET.close()
        return
    msg_received = ""
    for i in range(msg_length):
        msg_received += SOCKET.recv(1).decode("utf-8")

    if msg_received == "Error 404":
        print(f"{email} was not found in the database!")
    else:
        print(f"{email} belongs to {msg_received}")
    # If the user wants to search other emails?
    ask = input("Do you want to search another email?[y/n] ")
    if ask.lower() in ["y", "yes"]:
        send_message()
    else:
        print("Aborting program...")

create_socket()
send_message()