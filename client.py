import socket, sys

HOST = "68.183.131.122"  # Public IP Address of Digital Ocean droplet / Server running server.py
PORT = 8080
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a TCP socket to be used over ipv4
try:
    SOCKET.connect((HOST, PORT))  # Connects to the server via socket
except:
    print("Error connecting to the server. Check server connection")
    sys.exit(1)

def send():
    email = input("Enter an email to search in the database")
    SOCKET.send(b"Q")  # Q denotes this is a query type
    SOCKET.send(bytes(len(email)))  # sending the length of email
    SOCKET.send(email.encode("utf-8"))

send()