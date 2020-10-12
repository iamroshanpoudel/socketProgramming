import socket

HOST = socket.gethostbyname(socket.gethostname() + ".local")  # Fetches the public ip address of the client
print(HOST)