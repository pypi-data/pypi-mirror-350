import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def fill_missing(df, method='mean'):
    df = df.copy()
    for col in df.columns:
        if df[col].isnull().any():
            if method == 'mean' and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            elif method == 'median' and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            elif method == 'mode':
                df[col] = df[col].fillna(df[col].mode()[0])
            else:
                df[col] = df[col].fillna(method)
    return df

def drop_duplicates(df):
    return df.drop_duplicates()

def encode_categorical(df, columns):
    df = df.copy()
    le = LabelEncoder()
    for col in columns:
        if col in df.columns:
            df[col] = le.fit_transform(df[col].astype(str))
    return df

def scale_columns(df, columns):
    df = df.copy()
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df
