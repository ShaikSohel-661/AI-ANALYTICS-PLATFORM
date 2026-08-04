import pandas as pd

def column_analysis(df):
    column_info = []
    for column in df.columns:
        col_data = df[column]
        col_info = {
            "column_name": column,
            "data_type": col_data.dtype,
            "missing_values": col_data.isnull().sum(),
            "unique_values": col_data.nunique(),
            "top_value": col_data.mode()[0] if not col_data.mode().empty else None,
            "top_value_count": col_data.value_counts().iloc[0] if not col_data.value_counts().empty else 0
        }
        column_info.append(col_info)
    return pd.DataFrame(column_info)
