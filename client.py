import socket

HOST = "68.183.131.122"  # Public IP Address of Digital Ocean droplet / Server running server.py
PORT = 8080
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a TCP socket to be used over ipv4
SOCKET.connect((HOST, PORT))  # Connects to the server via socket

