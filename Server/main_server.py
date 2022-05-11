"""
Created on 2022-05-07

Author: Mohammad Amin Movahedi Moghadam
Email: antonio1384minkowski@zohomail.eu
"""

import socket 
import sys 
import os 
import threading
from FTP_Server.FTP import *
from DataSet_Reader.DataReader import Reader
from config_generator.config_gen import config
from Client_multihandler_trainer.trainer_multihandler import client_handler_train
from Client_multihandler_receiver.multihandler_receiver import client_handler_recv

# Initialize main server variables
BUFFER              = 4096
FORMAT              = 'utf-8'
DISCONNECT_MESSAGE  = '!DISCONNECT'
HOST                = input('Enter Server IP: ')
PORT                = int(input('Enter Server Port: '))
status              = input('Do you wanna start training? <Y/n>: ')

# Create the server TCP socket object and bind that
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
print('[*] Server builded...')

if status == 'n':
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_handler_recv, args=[conn, addr, status])
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

# Main model parameters
model_name          = input("Enter model file's name: ")
model_path          = os.getcwd() + '/model/' + model_name
num_of_clients      = int(input('Enter number of clients: '))
num_of_epochs       = int(input("Enter number of epochs: "))
num_of_batchsize    = int(input('Enter number of batchsize: '))
optimizer           = input('Enter optimizer method: ')
loss_func           = input('Enter loss function: ')
config_path         = os.getcwd() + '/config/config.sql'

# Convert Numpy array into batches
def array2batch(dataset, num_of_clients):
    BATCH_SIZE = int(len(dataset) / num_of_clients)
    batches = []
    
    for offset in range(0, len(dataset), BATCH_SIZE):
        batches.append(dataset[offset: offset + BATCH_SIZE])

    return batches

print('''

if you wanna send your custom dataset in .csv, .xlsx or .npz from server to clients enter "1"
if you wanna use a dataset thats already exists in "dataset" folder in clients enter "2"
if you wanna use a local tensorflow's dataset enter "3"

''')

dataset_status = int(input('>> '))

if dataset_status == 1:
    X, Y = Reader()
    X_Batch, Y_Batch = array2batch(X, num_of_clients), array2batch(Y, num_of_clients)
    dataset = [X_Batch, Y_Batch]
    dataset_length = None 
    print('\n' * 50)

elif dataset_status == 2:
    dataset_length = None 
    print('\n' * 50)

elif dataset_status == 3:
    dataset = input("Enter dataset's name: ")
    dataset_length = input("Enter dataset's length: ")
    input_output_order = input('Enter the order of input data (X) and output data (Y): ')

    print('\n' * 50)

else:
    sys.exit('Try again and enter the correct answer')

# Create the main server function
def main(model_path, config_path, dataset_status, dataset, dataset_length):
    # Enabling our server to accept connections
    server.listen()
    print(f'[START] Server started listening on {HOST}:{PORT}')

    # Set a index for batches
    index = 0

    while True:
        # Check if all of clients connected to the server and received the model and dataset, shutting down the server
        if index == num_of_clients:
            sys.exit('[FINISH] Model and dataset broadcasting was finished')

        conn, addr = server.accept()

        # Send dataset from server to the clients into batches
        if dataset_status == 1:
            thread = threading.Thread(target=client_handler_train, args=(conn, addr, model_path, config_path, dataset_status, dataset[index], status)) 

        # Dataset has already existed on clients
        elif dataset_status == 2:
            thread = threading.Thread(target=client_handler_train, args=(conn, addr, model_path, config_path, dataset_status, dataset, status)) 

        # We wanna use a dataset which is already has axisted on tensorflow api and we send the name of that dataset and batch of that
        else:
            # Calculating batch size for each client
            BATCH_SIZE = int(int(dataset_length) / int(num_of_clients))
            START = index * BATCH_SIZE
            END = START + BATCH_SIZE
            Batch = [START, END, input_output_order]
            print(Batch)

            thread = threading.Thread(target=client_handler_train, args=(conn, addr, model_path, config_path, dataset_status, dataset, status, Batch))

        index += 1

        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

# Generate the config sqlite file
config(num_of_epochs, num_of_batchsize, optimizer, loss_func)
main(model_path, config_path, dataset_status, dataset, dataset_length)