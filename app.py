import streamlit as st
from utils.data_loader import load_data
from utils.data_analysis import analyze_df
from utils.col_analysis import column_analysis
from utils.data_cleaning import summarize_data

st.set_page_config(page_title="AI Analytics Platform", page_icon="📊", layout="wide")

st.title("AI Analytics Platform 📊")


data_file = st.file_uploader("Upload your CSV or Excelfile ", type=["csv", "xlsx"])


if data_file is not None:
    df = load_data(data_file)
    if df is not None:
        st.success("File uploaded successfully! ✅") ## display the dataframe if the file is uploaded successfully
        st.dataframe(df)
        
        # data analysis section
        analysis = analyze_df(df)

        st.subheader("📊 Dataset Overview")
        #data analysis metrics in columns

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Rows", analysis["rows"])
        col2.metric("Columns", analysis["columns"])
        col3.metric("Missing Values", analysis["missing"])
        col4.metric("Duplicates", analysis["duplicates"])
        col5.metric("Memory Usage", f'{analysis["memory"]} MB')

        #column analysis
        st.subheader("📋 Column Analysis")
        col_analysis_df = column_analysis(df)
        st.dataframe(col_analysis_df)

        #summary of the dataset using AI
        context = {
            "analysis": analysis,
            "column_info": col_analysis_df
        }
        ai_summary = summarize_data(context)
        st.subheader("📝 Dataset Summary")

        



    else:
        st.error("Failed to load the data. Please check the file format and try again.")


