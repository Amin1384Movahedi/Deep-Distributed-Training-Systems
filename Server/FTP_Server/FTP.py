import os 

# This FTP module will send model file in .h5 format and config thats include number of epochs, 
# batch_size, optimizer algorithm and loss function.
# also Receiver function will receive trained model file in .h5 format and training logs in .zip format.

# Create the Sender function
def FTP_Sender(conn, path, data=None):
    print(f'\n\n================ File Transfer Sender Protocol ================\n')
    print('Wating for command.\n')

    # Make sure the path of file we wanna send, exists
    print(f'File path verification for {path}.')
    if not os.path.exists(path):
        return f'{path} Not found!'

    # Extract file name from file path
    print("Extracting the file's name from path.\n")
    filename = os.path.basename(path)

    # Create the Sender loop
    while True:
        # Wait for command
        print("Waiting for client's FTP requests.\n")
        cmd = conn.recv(32).decode('utf-8')

        # Sending the file's name
        if cmd == 'getfilename':
            print('"getfilename" command received.')
            conn.sendall(filename.encode('utf-8'))

        # Start sending the file
        if cmd == 'getfile':
            print('"getfile" command received. Going to send file.')

            if not data:
                with open(path, 'rb') as f:
                    data = f.read()

            conn.sendall(f"{'%16d' % len(data)}".encode('utf-8'))
            conn.sendall(data)
            print('File transmission done.')

        # Breaking the loop when file transmission is completed.
        if cmd == 'end':
            print('"end" command received. Teminate.\n\n')
            break

# Create the Receiver function
def FTP_Receiver(conn):
    print(f'\n\n================ File Transfer Receiver Protocol ================\n')

    # Initializing pathes variables
    log_path = os.getcwd() + '/log'
    pre_trained_path = os.getcwd() + '/pre_trained_models'

    print('Going to receive file.')

    # Sending the "getfilename" command and waiting to receiving the filename
    conn.sendall('getfilename'.encode('utf-8'))
    filename = conn.recv(1024).decode('utf-8')

    print(f'File Name: {filename}\n')

    # Make sure the needed pathes are existing
    print(f'path verification for {log_path} ...')
    if not os.path.exists(log_path):
        print(f"{log_path} wasn't exsist, start creating a log folder.")
        os.mkdir('log')
        print('Log folder created!\n')

    print(f'path verification for {pre_trained_path} ...')
    if not os.path.exists(pre_trained_path):
        print(f"{pre_trained_path} wasn't exsist, start creating a pre trained models folder.")
        os.mkdir('pre_trained_models')
        print('pre trained models folder created!\n')

    # Separating save path by formates
    if filename.endswith('_model.zip'):
        save_path = f'{pre_trained_path}/{filename}'

    else:
        save_path = f'{log_path}/{filename}'

    print('Filename: ' + filename)

    # Start receiving and writing file
    print(f'Start receiving the {filename} file.')
    with open(save_path, 'wb') as f:
        while True:
            conn.sendall('getfile'.encode('utf-8'))
            size = int(conn.recv(16).decode('utf-8'))
            print('Total size: ' + str(size))
            recvd = b''
            while size > len(recvd):
                data = conn.recv(1024)
                if not data: 
                    break
                recvd += data
                f.write(data)
            break

    # End of Receiving
    conn.sendall('end'.encode('utf-8'))
    print('File received.\n\n')