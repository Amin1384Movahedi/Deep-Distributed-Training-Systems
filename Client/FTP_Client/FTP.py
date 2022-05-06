import os 
import socket

# This FTP module will recive model file in .h5 format and config thats includes num of epochs, 
# batch_size, optimizer algorithm and loss function.
# also Sender function will send trained model file in .h5 format and training logs in .zip format.

# Create the Receiver function
def FTP_Receiver(conn):
    # Initializing pathes variables
    model_path = os.getcwd() + '/model'
    config_path = os.getcwd() + '/config'
    dataset_path = os.getcwd() + '/dataset'

    print('Going to receive file.')

    # Sending the "getfilename" command and waiting to receiving the filename
    conn.sendall('getfilename'.encode('utf-8'))
    filename = conn.recv(1024).decode('utf-8')

    # Make sure the needed pathes are existing
    if not os.path.exists(model_path):
        os.mkdir('model')

    if not os.path.exists(config_path):
        os.mkdir('config')

    if not os.path.exists(dataset_path):
        os.mkdir('dataset')

    # Separating save path by formates
    if filename.endswith('.h5'):
        save_path = f'{model_path}/{socket.gethostname()}.h5'

    elif filename.endswith('.sql'):
        save_path = f'{config_path}/config.sql'

    elif filename.endswith('.npz'):
        if filename.startswith('Input'):
            save_path = f'{dataset_path}/X/{filename}'
        
        elif filename.startswith('Outout'):
            save_path = f'{dataset_path}/Y/{filename}'
    
    print('Filename: ' + filename)

    # Start receiving and writing file
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
    print('Wating for command.')

    # Make sure the path of file we wanna send, exists
    if not os.path.exists(path):
        return f'{path} Not found!'

    # Extract file name from file path
    filename = os.path.basename(path)

    # Create the Sender loop
    while True:
        # Wait for command
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
            print('"end" command received. Teminate.')
            break