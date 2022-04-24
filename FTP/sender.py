import socket 
import os 
import tqdm 

def FTP_Sender(path, conn, addr):
    # Initialize main FTP Server variables
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    FORMAT              = 'utf-8'

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