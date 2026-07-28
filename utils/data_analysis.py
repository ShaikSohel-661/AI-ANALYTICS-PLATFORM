import pandas as pd

def analyze_df(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing": df.isnull().sum().sum(),
        "duplicates": df.duplicated().sum(),
        "memory": round(df.memory_usage(deep=True).sum()/ 1024**2, 2)
    }