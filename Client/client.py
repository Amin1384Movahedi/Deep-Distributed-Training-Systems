import socket 
from DataSet_Reader.DataReader import Reader
import random
from train_module.trainer import train
import tensorflow as tf 
from sklearn.model_selection import train_test_split
from FTP_Client.FTP import * 
import pickle
from zipper.zipper import zip_log

# Initialize main client variables
BUFFER    = 4096 
FORMAT    = 'utf-8'
HOST      = input('Enter the server ip: ')
PORT      = int(input('Enter the server port: '))
DISCONNECT_MESSAGE  = '!DISCONNECT'

# Build the client socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
print('[*] Connecting to the server...')
client_socket.connect((HOST, PORT))
print(f'[CONNECTED] Connection to the {HOST}:{PORT} wass successful')

# Receiving status and sending a response
status = client_socket.recv(10).decode(FORMAT)
client_socket.sendall('status code received!'.encode(FORMAT))

if status == 'Y':
    # Start receiving the model file and configs 
    FTP_Receiver(client_socket)
    FTP_Receiver(client_socket)

    # Receiving dataset status
    client_socket.sendall('getdataset_status'.encode(FORMAT))
    dataset_status = int(client_socket.recv(32).decode(FORMAT))

    if dataset_status == 1:
        # Sending "getdataset" command for receiving the dataset
        client_socket.sendall('getdataset'.encode(FORMAT))

        # Start Receiving X data (input data)
        X = FTP_Receiver(client_socket) 

        # Start receiving Y data (output data)
        Y = FTP_Receiver(client_socket) 

        # Send disconnect command and disconnecting from server and start training
        client_socket.sendall(DISCONNECT_MESSAGE.encode(FORMAT))

        # Split X and Y received data into train and test data
        X_train, Y_train, X_test, Y_test = train_test_split(X, Y, test_size=0.3, random_state=random.randint(20, 60))

        # Start training by received data
        train(X_train, Y_train, X_test, Y_test)

    elif dataset_status == 2:
        # Sending "getdataset" command for receiving the dataset
        client_socket.sendall('getdataset'.encode(FORMAT))

        client_dataset = client_socket.recv(25).decode(FORMAT)

        # Send disconnect command and disconnecting from server and start training
        client_socket.sendall(DISCONNECT_MESSAGE.encode(FORMAT))

        # Reading dataset from local folders
        X, Y = Reader()

        # Split the data into train and test
        X_train, Y_train, X_test, Y_test = train_test_split(X, Y, test_size=0.3, random_state=random.randint(20, 60))

        train(X_train, Y_train, X_test, Y_test)

    else: 
        # Sending "getdataset" command for receiving the dataset
        client_socket.sendall('getdataset'.encode(FORMAT))

        # Start receiving training dataset part and sending a done response
        dataset_size = pickle.loads(client_socket.recv(BUFFER))
        client_socket.sendall("Dataset batch received!".encode(FORMAT))

        # Start receiving dataset name
        dataset_name = client_socket.recv(BUFFER).decode(FORMAT)
        client_socket.sendall('Dataset name received!'.encode(FORMAT))

        # Send disconnect command and disconnecting from server and start training
        client_socket.sendall(DISCONNECT_MESSAGE.encode(FORMAT))

        # Loading dataset from tensorflow
        dataset_loader_query = f"(X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.{dataset_name}.load_data()"
        exec(dataset_loader_query)
        START, END, input_output_order = dataset_size[0], dataset_size[1], dataset_size[2]

        # Inizializing train function with different inputs and outputs and start training
        if input_output_order  == 'XX':
            train(X_train[START:END], X_train[START:END], X_test[START:END], X_test[START:END]) 

        else:
            train(X_train[START:END], Y_train[START:END], X_test[START:END], Y_test[START:END]) 

else:
    # Zipping the log folder
    zip_log()
    
    # Initializing log path and model path
    log_path = f'{os.getcwd()}/{socket.gethostname()}_log.zip'
    trained_model_path = f'{os.getcwd()}/model/{socket.gethostname()}.h5'

    # Waiting for "gettrained_model" command and Sending trained model 
    cmd = client_socket.recv(30).decode(FORMAT)
    if cmd == 'gettrained_model':
        FTP_Sender(client_socket, trained_model_path)

    # Waiting for "getlog" command and Sending log
    cmd = client_socket.recv(30).decode(FORMAT)
    if cmd == 'getlog':
        FTP_Sender(client_socket, log_path)