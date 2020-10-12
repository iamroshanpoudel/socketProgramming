import socket, threading

HOST = "68.183.131.122" # Public IP of digital ocean droplet / use your server address
PORT = 8080
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a TCP socket to be used over ipv4
SOCKET.bind((HOST, PORT))  # Binds the ip address of server with the port number
BUFFER_SIZE = 256 # Maximum Query/Response size in bytes

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
        print("[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}") # Active connections = Total threads - 1

def handle_client(conn, addr):
    """Handles each client"""
    msg_type = conn.recv(1).decode("utf-8")  # First byte contains message Type
    str_len = conn.recv(1).decode("utf-8")  # Second byte contains string length
    if (msg_type != "Q" or not str_len):
        return
    print("Str_len: {str_len}")
    str_len = int(str_len)

    msg = ""
    while (len(msg) != str_len):
        msg_chunk = conn.recv(BUFFER_SIZE).decode("utf-8")
        if msg_chunk == "":
            break
        msg += msg_chunk
        print(msg)
    conn.close()


handle_connections()
    
