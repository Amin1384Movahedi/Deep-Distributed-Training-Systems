import socket 

# Initialize main client variables
BUFFER              = 64
FORMAT              = 'utf-8'
DISCONNECT_MESSAGE  = '!DISCONNECT'
HOST                = input('Enter Server IP: ')
PORT                = int(input('Enter Server Port: '))

# Build our client socket object and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

