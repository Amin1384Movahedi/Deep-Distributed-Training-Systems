import socket 
import sys 
import os 
import sqlite3
import threading
from FTP_Server.FTP import *
from DataSet_Reader.DataReader import Reader

# Initialize main server variables
BUFFER              = 4096
FORMAT              = 'utf-8'
DISCONNECT_MESSAGE  = '!DISCONNECT'
HOST                = input('Enter Server IP: ')
PORT                = int(input('Enter Server Port: '))
model_name          = input('Enter model file name: ')
num_of_clients      = int(input('Enter number of clients: '))
num_of_epochs       = int(input("Enter number of epochs: "))
num_of_batchsize    = int(input('Enter number of batchsize:'))
optimizer           = input('Enter optimizer method: ')
loss_func           = input('Enter loss function: ')

print('''

if you wanna send your custom dataset in .csv, .xlsx or .npz from server to clients enter "1"
if you wanna use a dataset thats already exists in "dataset" folder in clients enter "2"
if you wanna use a local tensorflow's dataset enter "3"

''')

dataset_status      = int(input('>> '))

if dataset_status == 1:
    dataset_path = input('Enter your dataset path: ')
    dataset = Reader(dataset_path)
    print('\n' * 10)

elif dataset_status == 2:
    print('\n' * 10)

elif dataset_status == 3:
    dataset = input("Enter dataset's name: ")
    length_of_dataset = input("Enter dataset's length: ")

else:
    sys.exit('Try again and enter the correct answer')

# Convert Numpy array into batches
def array2batch(dataset, num_of_clients):
    BATCH_SIZE = int(len(dataset) / num_of_clients)
    batches = []
    
    for offset in range(0, len(dataset), BATCH_SIZE):
        batches.append(dataset[offset: offset + BATCH_SIZE])

    return batches

# Creating a function to save a sql file that's includes number of epochs, batch_size, optimizer method and loss function
def config(num_of_epochs, num_of_batchsize, optimizer, loss_func):
    if not os.path.exists('config'):
        os.mkdir('config')

    # Removing the sqlite database file if it's exists and creating another
    config_sqlite_path = os.getcwd() + '/config/config.sql'
    if os.path.exists(config_sqlite_path):
        os.remove(config_sqlite_path)

    # Connect to the database
    con = sqlite3.connect(config_sqlite_path)
    c = con.cursor()
    print('[DATABASE CONNECTION] Connected to the sqlite database successfully')

    # Creating config tables
    query = '''create table config(
        epochs INTEGER(20),
        batch_size INTEGER(50),
        optimizer TEXT(100),
        loss_function TEXT(100)
    )'''

    try:
        c.execute(query)
        con.commit()

    except:
        print('[ERROR] Something went wrong')
        con.rollback()
        con.close()
        sys.exit()

    # Inserting configs into table
    query = f'''insert into config VALUES ({num_of_epochs}, {num_of_batchsize}, {optimizer}, {loss_func}'''

    try:
        c.execute(query)
        con.commit()

    except:
        print('[ERROR] Something went wrong')
        con.rollback()
        con.close()
        sys.exit()

    print('[SUCCESSFUL] sqlite config file generated successfully')


# Create the server TCP socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.build((HOST, PORT))
print('[*] Server builded...')

# Create the client handler function
def client_handler(conn, addr, send_dataset, use_exists_dataset, use_tensorflow_dataset):
    print(f'[NEW CONNECTION] {addr} connected.')

    # Create the handler loop
    connected = True
    while connected:
        msg_length = int(conn.recv(BUFFER).decode(FORMAT))
        msg = conn.recv(msg_length).decode(FORMAT)

        if msg == DISCONNECT_MESSAGE:
            connected = False 

        print(f'{addr} {msg}')

    # Close connection after disconnecting
    conn.close()

# Create the main server function
def main():
    # Enabling our server to accept connections
    server.listen()
    print(f'[START] Server started listening on {HOST}:{PORT}')

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_handler, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

# Generate the config sqlite file
config(num_of_epochs, num_of_batchsize, optimizer, loss_func)
main()