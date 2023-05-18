import pandas as pd
import re

def pre_process():
    data = pd.read_csv("~/ip_files/or.csv")
    data['Description'] = data['Description'].str.replace('\W', '')

    if data.isnull().values.any():
        data=data.dropna(axis=0, how='any')

    data.to_csv("~/ip_files/or1.csv")