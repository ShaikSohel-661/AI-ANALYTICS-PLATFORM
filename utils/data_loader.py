import pandas as pd


def load_data(data_file):
    try:
        if data_file.name.endswith('.csv'):
        
            return pd.read_csv(data_file) 

        elif data_file.name.endswith('.xlsx'):

            return pd.read_excel(data_file)
    except Exception as e:
         print(f"Error loading data: {e}")
         return None
