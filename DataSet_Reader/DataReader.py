import pandas as pd
from dask import dataframe as dd
import numpy as np
import os

# Create our Dataset Reader function
def Reader(path):
    # Make sure the name of file we want to read is exists
    if not os.path.exists(path):
        return f'{path} not found!'

    # Remove absolute path if there is
    filename = os.path.basename(path)

    # Check dataset for csv, json, excel and npz formats and read them
    if filename.endswith('.csv'):
        data = dd.read_csv(path)

    elif filename.endswith('.json'):
        data = dd.read_json(path)

    elif filename.endswith('.xlsx'):
        data = pd.read_excel(path)

    elif filename.endswith('.npz'):
        data = np.load(path)

    else:
        return f'{path} Unreadable!'

    return data