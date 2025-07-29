import pandas as pd

def load_csv(filepath):
    return pd.read_csv(filepath)

def load_excel(filepath):
    return pd.read_excel(filepath)

def load_json(filepath):
    return pd.read_json(filepath)
