import os 
import socket
import sys

# This FTP module will recive model file in .h5 format and config thats includes num of epochs, 
# batch_size, optimizer algorithm and loss function.
# also Sender function will send trained model file in .h5 format and training logs in .zip format.

# Create the Receiver function
def FTP_Receiver(conn):
    print(f'\n\n================ File Transfer Receiver Protocol ================\n')

    # Initializing pathes variables
    model_path = os.getcwd() + '/model'
    config_path = os.getcwd() + '/config'
    input_dataset_path = os.getcwd() + '/dataset/X'
    output_dataset_path = os.getcwd() + '/dataset/Y'

    print('Going to receive file.')

    # Sending the "getfilename" command and waiting to receiving the filename
    print(f'Sending the "getfilename" request to the server.')
    conn.sendall('getfilename'.encode('utf-8'))
    filename = conn.recv(1024).decode('utf-8')
    print(f"File's name received: {filename}\n")

    # Make sure the needed pathes are existing
    print(f'File path verification for {model_path}')
    if not os.path.exists(model_path):
        print(f"{model_path} wasn't exist, start creating a model folder.")

        os.mkdir('model')

        print('Model folder created!\n')

    print(f'File path verification for {config_path}')
    if not os.path.exists(config_path):
        print(f"{config_path} wasn't exist, start creating a config folder.")

        os.mkdir('config')

        print('Config folder created!\n')

    print(f'File path verification for {input_dataset_path}')
    if not os.path.exists(input_dataset_path):
        print(f"{input_dataset_path} wasn't exist, start creating a input dataset folder.")

        os.mkdir('dataset')

        print('Input dataset folder created!\n')

    print(f'File path verification for {output_dataset_path}')
    if not os.path.exists(output_dataset_path):
        print(f"{output_dataset_path} wasn't exist, start creating a output dataset folder.")

        os.mkdir('dataset')

        print('Output dataset folder created!\n')

    # Separating save path by formates
    if filename.endswith('.h5'):
        save_path = f'{model_path}/{socket.gethostname()}.h5'

    elif filename.endswith('.sql'):
        save_path = f'{config_path}/config.sql'

    elif filename.endswith('.npz'):
        if filename.startswith('Input'):
            save_path = f'{input_dataset_path}/{filename}'
        
        elif filename.startswith('Outout'):
            save_path = f'{output_dataset_path}/{filename}'
    
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
    print('File received.')

# Create our Sender function
def FTP_Sender(conn, path, data=None):
    print(f'\n\n================ File Transfer Sender Protocol ================\n')
    print('Wating for command.\n')

    # Make sure the path of file we wanna send, exists
    print(f'File path verification for {path}.')
    if not os.path.exists(path):
        sys.exit(f'{path} Not found!') 

    # Extract file name from file path
    print("Extracting the file's name from path.\n")
    filename = os.path.basename(path)

    # Create the Sender loop
    while True:
        # Wait for command
        print("Waiting for server's FTP requests.\n")
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