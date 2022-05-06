import sqlite3
import os
import sys

# Load the config file
def load():
    path = os.getcwd() + '/config/config.sql'

    # Connect to the sqlite file
    con = sqlite3.connect(path)
    c = con.cursor()
    print('[CONNECTION TO SQLITE] Successfully connected to the sqlite')

    # Extract train parameters from sqlite
    query = '''select * from config'''

    # Execute the sqlite query
    try:
        c.execute(query)
        parameters = c.fetchone()
    except:
        sys.exit('[ERROR] Something went wrong in extracting')

    con.close()
    return parameters