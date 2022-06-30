"""
Created on 2022-05-07

Author: Mohammad Amin Movahedi Moghadam
Zohomail: amin1384movahedi@zohomail.com
Gmail: amin1384movahedi@gmail.com
"""

import socket 
from DataSet_Reader.DataReader import Reader
import random
from train_module import trainer
import tensorflow as tf 
from sklearn.model_selection import train_test_split
from FTP_Client.FTP import * 
import pickle
from zipper.zipper import zip_log, zip_model
import sys

# Initialize main client variables
BUFFER              = 4096 
FORMAT              = 'utf-8'
HOST                = input('Enter the server ip: ')
PORT                = int(input('Enter the server port: '))
DISCONNECT_MESSAGE  = '!DISCONNECT'
REFUSED_MESSAGE     = '!Connection_Refused'
ACCEPTED_MESSAGE    = '!Connection_Accepted'

# Build the client socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
print('\n[*] Connecting to the server...')
client_socket.connect((HOST, PORT))
print(f'[CONNECTED] Connection to the {HOST}:{PORT} wass successful\n')


# Waiting for "get_passphrase" command and sending the entered passphrase
# if the passphrase is correct, client can connect to the server and if client
# entered the passphrase wrong, client will get disconnected, and if client
# entered the passphrase wrong for 3 times, client cant connect to the server any more.
print('Waiting for "get_passphrase" command.')
cmd = client_socket.recv(50).decode(FORMAT)
if cmd == 'get_passphrase':
    passphrase = input("Enter server's passphrase: ").encode(FORMAT) 
    client_socket.sendall(passphrase)

print('\n\nWaiting for passphrase server authorization.')
cmd = client_socket.recv(50).decode(FORMAT)
if cmd == REFUSED_MESSAGE:
    client_socket.close()
    sys.exit('Passphrase is incorrect or you are banned from the server')

# Waiting for accept or refuse message, if client connected to the server and received
# the model and the dataset, client will receive refuse message, else client will
# receive the accept message and start receiving the model and the dataset.
print('Waiting for duplicated connection authorization.\n')
cmd = client_socket.recv(50).decode(FORMAT)
if cmd == REFUSED_MESSAGE:
    client_socket.close()
    sys.exit('You are connected to the server and received the model \nand the dataset already, you cant connect to the server \nand receive the model and the dataset any more.')

# Sending "getstatus_code" request to the server, receiving status and sending a response
print('Receiving the status code.')
client_socket.sendall('getstatus_code'.encode(FORMAT))
status = client_socket.recv(10).decode(FORMAT)
client_socket.sendall(f'[{socket.gethostname()}] status code received!'.encode(FORMAT))

if status == 'y':
    # Start receiving the model file and configs 
    FTP_Receiver(client_socket)
    FTP_Receiver(client_socket)

    # Receiving dataset status
    print('Sending the "getdataset_status" request to the server.\n\n')
    client_socket.sendall('getdataset_status'.encode(FORMAT))
    dataset_status = int(client_socket.recv(32).decode(FORMAT))

    print('Sending the "getdataset" request to the server.')
    # Sending "getdataset" command for receiving the dataset
    client_socket.sendall('getdataset'.encode(FORMAT))
    
    print('Start receiving the dataset from server.')
    if dataset_status == 1:
        # Start Receiving X data (input data)
        X = FTP_Receiver(client_socket) 

        # Start receiving Y data (output data)
        Y = FTP_Receiver(client_socket) 

        # Send disconnect command and disconnecting from server and start training
        client_socket.sendall(DISCONNECT_MESSAGE.encode(FORMAT))

        # Split X and Y received data into train and test data
        X_train, Y_train, X_test, Y_test = train_test_split(X, Y, test_size=0.3, random_state=random.randint(20, 60))

        # Start training by received data
        trainer.train(X_train, Y_train, X_test, Y_test)

    elif dataset_status == 2:
        client_dataset = client_socket.recv(25).decode(FORMAT)

        # Send disconnect command and disconnecting from server and start training
        client_socket.sendall(DISCONNECT_MESSAGE.encode(FORMAT))

        # Reading dataset from local folders
        X, Y = Reader()

        # Split the data into train and test
        X_train, Y_train, X_test, Y_test = train_test_split(X, Y, test_size=0.3, random_state=random.randint(20, 60))

        trainer.train(X_train, Y_train, X_test, Y_test)

    else: 
        # Check for log folder
        log_path = os.getcwd() + '/log'
        if not os.path.exists(log_path):
            os.mkdir('log')

        # Start receiving training dataset part and sending a done response
        dataset_size = pickle.loads(client_socket.recv(BUFFER))
        client_socket.sendall("Dataset batch received!".encode(FORMAT))

        # Start receiving dataset name
        dataset_name = client_socket.recv(BUFFER).decode(FORMAT)
        client_socket.sendall('Dataset name received!'.encode(FORMAT))

        # Send disconnect command and disconnecting from server and start training
        client_socket.sendall(DISCONNECT_MESSAGE.encode(FORMAT))

        # Loading dataset from tensorflow
        try:
            dataset_loader_query = f"(X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.{dataset_name}.load_data()"
            exec(dataset_loader_query)
            START, END, input_output_order = dataset_size[0], dataset_size[1], dataset_size[2]

        except Exception as e:
            with open(f'{log_path}/training_exception.log', 'w') as f:
                f.write(str(e))

        # Inizializing train function with different inputs and outputs and start training
        if input_output_order  == 'XX':
            trainer.train(X_train[START:END], X_train[START:END], X_test[START:END], X_test[START:END]) 

        else:
            trainer.train(X_train[START:END], Y_train[START:END], X_test[START:END], Y_test[START:END]) 

elif status == 'n':
    # Zipping the log and model folder
    print('Zipping the log folder and pre trained models folder\n')
    zip_log()
    zip_model()
    
    # Initializing log path and model path
    log_path = f'{os.getcwd()}/{socket.gethostname()}_log.zip'
    trained_model_path = f'{os.getcwd()}/{socket.gethostname()}_model.zip'

    # Waiting for "gettrained_model" command and Sending trained model 
    print('Waiting for "gettrained_model" command.')
    cmd = client_socket.recv(30).decode(FORMAT)
    if cmd == 'gettrained_model':
        print('Start sending the pre trained models in a zip file.\n')
        FTP_Sender(client_socket, trained_model_path)

    # Waiting for "getlog" command and Sending log
    print('Waiting for "getlog" command.')
    cmd = client_socket.recv(30).decode(FORMAT)
    if cmd == 'getlog':
        print('Start sending the logs in a zip file.\n')
        FTP_Sender(client_socket, log_path)
