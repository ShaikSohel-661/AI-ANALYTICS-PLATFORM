from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)
print("Using NEW SDK")
print("API Key:", os.getenv("GOOGLE_API_KEY")[:10])


def summarize_data(context):
    analysis = context["analysis"]
    column_info = context["column_info"]


    prompt = f"""
    You are as senior data analyst. Analyze the dataset summary.
    You have been given a dataset with the following characteristics:
    -Rows: {analysis["rows"]}
    -columns: {analysis["columns"]}
    -Missing Values: {analysis["missing"]}
    -Duplicates: {analysis["duplicates"]}

    Columns Information:
    {column_info.to_dict(orient='records')}


    Please provide a concise summary of the dataset, highlighting any potential issues, trends, or insights that can be derived from the data.
    Your summary should be clear and actionable for stakeholders who may not have a technical background.
    Keep these points in mind while generating the summary:
    1. What type of dataset is this?
    2. Give a concise summary.
    3. Identify data quality issues.
    4. Recommend cleaning steps.
    5. Suggest useful analyses or visualizations.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
        )
    return response.text




#def cleaned_data(df):
