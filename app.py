import streamlit as st

from utils.col_analysis import column_analysis
from utils.data_analysis import analyze_df
from utils.ai_summary import summarize_data
from utils.data_loader import load_data
from utils.data_cleaning import clean_data

st.set_page_config(page_title="AI Analytics Platform", page_icon="📊", layout="wide")

st.title("AI Analytics Platform 📊")


data_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if data_file is not None:
    df = load_data(data_file)
    if df is not None:
        st.success("File uploaded successfully! ✅")
        st.dataframe(df)

        analysis = analyze_df(df)

        st.subheader("📊 Dataset Overview")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Rows", analysis["rows"])
        col2.metric("Columns", analysis["columns"])
        col3.metric("Missing Values", analysis["missing"])
        col4.metric("Duplicates", analysis["duplicates"])
        col5.metric("Memory Usage", f'{analysis["memory"]} MB')

        st.subheader("📋 Column Analysis")
        col_analysis_df = column_analysis(df)
        st.dataframe(col_analysis_df)

        context = {
            "analysis": analysis,
            "column_info": col_analysis_df,
        }

        st.markdown("""
        <style>
        div.stButton > button {
            background-color: black;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }

        div.stButton > button:hover {
            background-color: #333333;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if "cleaned_df" not in st.session_state:
            st.session_state.cleaned_df = df.copy()

        if st.button("Generate AI Summary"):
            with st.spinner("Analyzing your dataset..."):
                ai_summary = summarize_data(context)
            
            if ai_summary.startswith("Unable to generate AI summary"):
                st.error(ai_summary)
            else:
                st.subheader("📝 Dataset Summary")
                st.markdown(ai_summary)
        

        
        instructions = st.text_area("Tell me how you want to clean the data")


        if st.button("Clean Data"):
            if instructions.strip():

                with st.spinner("Cleaning your dataset..."):
                    cleaned_df = clean_data(st.session_state.cleaned_df, instructions)

                if cleaned_df is not None:
                    st.session_state.cleaned_df = cleaned_df
                    st.success("Cleaning completed successfully.")
                    st.subheader("🧹 Cleaned Dataset")
                    st.dataframe(st.session_state.cleaned_df)
                else:
                    st.error("Data cleaning failed.")

            else:
                st.warning("Please enter cleaning instructions.")
                    

    else:
        st.error("Failed to load the data. Please check the file format and try again.")


