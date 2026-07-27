import streamlit as st
from utils.data_loader import load_data

st.set_page_config(page_title="AI Analytics Platform", page_icon="📊", layout="wide")

st.title("AI Analytics Platform 📊")


data_file = st.file_uploader("Upload your CSV or Excelfile ", type=["csv", "xlsx"])


if data_file is not None:
    df = load_data(data_file)
    if df is not None:
        st.success("File uploaded successfully! ✅")
        st.dataframe(df)

    else:
        st.error("Failed to load the data. Please check the file format and try again.")