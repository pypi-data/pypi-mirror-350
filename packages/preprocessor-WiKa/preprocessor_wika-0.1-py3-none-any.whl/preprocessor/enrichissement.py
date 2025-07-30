import pandas as pd 
def map_values(df, col, mapping):
    df[col] = df[col].map(mapping)
    return df


def encode_categorical(df, columns):
    return pd.get_dummies(df, columns=columns)