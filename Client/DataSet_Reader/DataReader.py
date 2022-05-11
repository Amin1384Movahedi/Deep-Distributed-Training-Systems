import pandas as pd
import numpy as np
import sys
import os
import random

# Create the Dataset Reader function
def Reader():
    # This function will extract all input data from dataset/X/
    def Read_X():
        # Make sure the name of file we wanna read, exists
        path = os.getcwd() + '/dataset/X'
        files = [f'{path}/{file}' for file in os.listdir(f'{path}/') if file.endswith('.csv') or file.endswith('.xlsx') or file.endswith('.npz')]

        if not os.path.exists(path):
            sys.exit(f'{path} not found!')

        if len(files) == 0:
            sys.exit('There is no available dataset files!')

        X = []

        # Check dataset for csv, excel and npz formats and read them
        for file in files:
            if file.endswith('.csv'):
                data = pd.read_csv(file).values 
                X.append(data)

            elif file.endswith('.xlsx'):
                data = pd.read_excel(file).values 
                X.append(data)

            elif file.endswith('.npz'):
                data = np.load(file)
                X.append(data)

            else:
                sys.exit(f'{file} is unreadable!')

        return random.shuffle(X)

    # This function will extract all output data from dataset/Y/
    def Read_Y():
        # Make sure the name of file we wanna read, exists
        path = os.getcwd() + '/dataset/Y'
        files = [f'{path}/{file}' for file in os.listdir(f'{path}/') if file.endswith('.csv') or file.endswith('.xlsx') or file.endswith('.npz')]

        if not os.path.exists(path):
            sys.exit(f'{path} not found!')

        if len(files) == 0:
            sys.exit('There is no available dataset files!')

        Y = []

        # Check dataset for csv, excel and npz formats and read them
        for file in files:
            if file.endswith('.csv'):
                data = pd.read_csv(file).values 
                Y.append(data)

            elif file.endswith('.xlsx'):
                data = pd.read_excel(file).values 
                Y.append(data)

            elif file.endswith('.npz'):
                data = np.load(file)
                Y.append(data)

            else:
                sys.exit(f'{file} is unreadable!')

        return random.shuffle(Y) 

    return Read_X(), Read_Y()