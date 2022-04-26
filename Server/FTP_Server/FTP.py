import socket 
import os 
import tqdm 

# This FTP module will send model file in .h5 format and config thats includes num of epochs, 
# batch_size, optimizer algorithm and loss function.
# alse Reciver function will recive trained model file in .h5 format and training logs in .zip format.

# Create our Sender function
def FTP_Sender(model_path, config_path, conn, addr):
    # Initialize main FTP Server variables
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    FORMAT      = 'utf-8'

    # Make sure the name of model file we want to send is exists
    if not os.path.exists(model_path):
        return f'{model_path} Not found!'

    print(f'[FTP] Sending model file to {addr}')

    # ============== Start sending model file ============== 
    # Get the model file size
    filesize = os.path.getsize(model_path)

    # Send model filesize
    conn.send(str(filesize).encode(FORMAT))

    # Start sending the model file
    progress = tqdm.tqdm(range(filesize), f"Sending {model_path}", unit="B", unit_scale=True, unit_divisor=1024)
    print(f'[START TRANSFER PROCESS] Sending model to {addr}')
    with open(model_path, "rb") as f:
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

    print(f'Model file was sended to {addr}')

    # ============== Start sending config file ============== 
    # Get the config file size
    filesize = os.path.getsize(config_path)

    # Send config filesize
    conn.send(str(filesize).encode(FORMAT))

    # Start sending the config file
    progress = tqdm.tqdm(range(filesize), f"Sending {config_path}", unit="B", unit_scale=True, unit_divisor=1024)
    print(f'[START TRANSFER PROCESS] Sending model to {addr}')
    with open(config_path, "rb") as f:
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

    print(f'Config file was sended to {addr}')

    return True

# Create our Reciver function
def FTP_Reciver(conn, addr):
    # Initialize main FTP Server variables
    # Receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR   = "<SEPARATOR>"
    FORMAT      = 'utf-8'

    # ============== Start reciving model file ============== 
    # Receive the trained model file infos
    # Receive using client socket, not server socket
    received = conn.recv(BUFFER_SIZE).decode(FORMAT)
    filename, filesize = received.split(SEPARATOR)

    # Remove absolute path if there is
    filename = os.path.basename(filename)

    # Convert to integer
    filesize = int(filesize)
    print(f'[START RECIVING] FileName: {filename}, Size: {filesize}')

    # Start receiving the trained model file from the socket and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # Read 1024 bytes from the socket (receive)
            bytes_read = conn.recv(BUFFER_SIZE)

            if not bytes_read:    
                # Nothing is received
                # File transmitting is done
                break

            # Write to the trained model file the bytes we just received
            f.write(bytes_read)

            # Update the progress bar
            progress.update(len(bytes_read))

    print(f'{filename} recived from {addr}')

    # ============== Start training logs file ============== 
    # Receive the training logs file infos
    # Receive using client socket, not server socket
    received = conn.recv(BUFFER_SIZE).decode(FORMAT)
    filename, filesize = received.split(SEPARATOR)

    # Remove absolute path if there is
    filename = os.path.basename(filename)

    # Convert to integer
    filesize = int(filesize)
    print(f'[START RECIVING] FileName: {filename}, Size: {filesize}')

    # Start receiving the training logs file from the socket and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # Read 1024 bytes from the socket (receive)
            bytes_read = conn.recv(BUFFER_SIZE)

            if not bytes_read:    
                # Nothing is received
                # File transmitting is done
                break

            # Write to the training logs file the bytes we just received
            f.write(bytes_read)

            # Update the progress bar
            progress.update(len(bytes_read))

    print(f'{filename} recived from {addr}')