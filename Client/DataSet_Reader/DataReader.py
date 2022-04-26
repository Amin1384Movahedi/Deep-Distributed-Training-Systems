import pandas as pd
from dask import dataframe as dd
import numpy as np
import os

# Create our Dataset Reader function
def Reader(path):
    # Make sure the name of file we want to read is exists
    if not os.path.exists(path):
        print(f'{path} not found!')
        return None

    # Remove absolute path if there is
    filename = os.path.basename(path)

    # Check dataset for csv, excel and npz formats and read them
    if filename.endswith('.csv'):
        data = dd.read_csv(path)

    elif filename.endswith('.xlsx'):
        data = pd.read_excel(path)

    elif filename.endswith('.npz'):
        data = np.load(path)

    else:
        print(f'{path} is unreadable!')
        return None

    return data