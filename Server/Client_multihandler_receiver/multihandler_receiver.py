from FTP_Server.FTP import *

# Initialize main server variables
BUFFER              = 4096
FORMAT              = 'utf-8'
DISCONNECT_MESSAGE  = '!DISCONNECT'

# Create the client handler function
def client_handler_recv(conn, addr, status):
    print(f'[NEW CONNECTION] {addr} connected.')
    
    # Sending status and receiving response
    conn.sendall(status.encode(FORMAT))
    response = conn.recv(30).decode(FORMAT)
    print(response)

    # Sending "gettrained_model" command to receive trained model from client
    conn.sendall('gettrained_model'.encode(FORMAT))
    FTP_Receiver(conn)

    # Sending "getlog" to recive logs from client
    conn.sendall('getlog'.encode(FORMAT))
    response = conn.recv(20).decode(FORMAT)

    print(response)

    FTP_Receiver(conn)

    conn.close()