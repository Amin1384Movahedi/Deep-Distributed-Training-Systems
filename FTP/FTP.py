import socket 
import os 
import tqdm 

# Create our Sender function
def FTP_Sender(path, conn, addr):
    # Initialize main FTP Server variables
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    FORMAT      = 'utf-8'

    # Make sure the name of file we want to send is exists
    if not os.path.exists(path):
        return f'{path} Not found!'

    print(f'[FTP] Sending model file to {addr}')

    # Get the file size
    filesize = os.path.getsize(path)

    # Send filesize
    conn.send(str(filesize).encode(FORMAT))

    # Start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {path}", unit="B", unit_scale=True, unit_divisor=1024)
    print(f'[START TRANSFER PROCESS] Sending model to {addr}')
    with open(path, "rb") as f:
        while True:
            # Read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)

            if not bytes_read:
                # File transmitting is done
                break

            # We use sendall to assure transimission in busy networks
            conn.sendall(bytes_read)

            # Update the progress bar
            progress.update(len(bytes_read))

    return f'Model file was sended to {addr}'

# Create our Reciver function
def FTP_Reciver(conn, addr):
    # Initialize main FTP Server variables
    # Receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR   = "<SEPARATOR>"
    FORMAT      = 'utf-8'

    # Receive the file infos
    # Receive using client socket, not server socket
    received = conn.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)

    # Remove absolute path if there is
    filename = os.path.basename(filename)

    # Convert to integer
    filesize = int(filesize)
    print(f'[START RECIVING] FileName: {filename}, Size: {filesize}')

    # Start receiving the file from the socket and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # Read 1024 bytes from the socket (receive)
            bytes_read = conn.recv(BUFFER_SIZE)

            if not bytes_read:    
                # Nothing is received
                # File transmitting is done
                break

            # Write to the file the bytes we just received
            f.write(bytes_read)

            # Update the progress bar
            progress.update(len(bytes_read))

    return f'{filename} recived from {addr}'