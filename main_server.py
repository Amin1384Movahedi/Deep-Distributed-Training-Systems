import socket 
import threading
from FTP.FTP import FTP_Sender

# Initialize main server variables
BUFFER              = 64
FORMAT              = 'utf-8'
DISCONNECT_MESSAGE  = '!DISCONNECT'
HOST                = input('Enter Server IP: ')
PORT                = int(input('Enter Server Port: '))

# Create the server TCP socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.build((HOST, PORT))
print('[*] Server builded...')

# Create the client handler function
def client_handler(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    # Create the handler loop
    connected = True
    while connected:
        msg_length = int(conn.recv(BUFFER).decode(FORMAT))
        msg = conn.recv(msg_length).decode(FORMAT)

        if msg == DISCONNECT_MESSAGE:
            connected = False 

        print(f'{addr} {msg}')

    # Close connection after disconnecting
    conn.close()

# Create tge main server function
def main():
    # Enabling our server to accept connections
    server.listen()
    print(f'[START] Server started listening on {HOST}:{PORT}')

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_handler, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

main()