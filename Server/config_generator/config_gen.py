import sqlite3
import sys 
import os 

# Creating a function to save a sql file that's includes number of epochs, batch_size, optimizer method and loss function
def config(num_of_epochs, num_of_batchsize, optimizer, loss_func, normalizer, train_method):
    if not os.path.exists('config'):
        os.mkdir('config')

    # Removing the sqlite database file, if it's exists and creating another
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
        loss_function TEXT(100),
        normalizer INTEGER(10),
        train_method INTEGER(20)
    )'''

    try:
        c.execute(query)
        con.commit()

    except:
        print('[ERROR] Something went wrong')
        con.rollback()
        con.close()
        sys.exit()

    # Inserting configs into the table
    query = f'''insert into config VALUES ({num_of_epochs}, {num_of_batchsize}, "{optimizer}", "{loss_func}", {normalizer}, {train_method})'''

    try:
        c.execute(query)
        con.commit()

    except:
        print('[ERROR] Something went wrong')
        con.rollback()
        con.close()
        sys.exit()

    print('[SUCCESSFUL] sqlite config file generated successfully')