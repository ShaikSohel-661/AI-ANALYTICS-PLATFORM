import os

from dotenv import load_dotenv
from google import genai
import sys

print("Python:", sys.executable)
print("GenAI module:", genai.__file__)

load_dotenv()


def get_client():
    api_key = os.getenv("GOOGLE_API_KEY") 
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY in the environment.")
    return genai.Client(api_key=api_key)


def _format_column_info(column_info):
    if hasattr(column_info, "to_dict"):
        return column_info.to_dict(orient="records")
    return column_info


def summarize_data(context):
    analysis = context.get("analysis", {})
    column_info = context.get("column_info", [])

    prompt = f"""
    You are a senior data analyst. Analyze the dataset summary.
    You have been given a dataset with the following characteristics:
    - Rows: {analysis.get('rows', 'n/a')}
    - Columns: {analysis.get('columns', 'n/a')}
    - Missing Values: {analysis.get('missing', 'n/a')}
    - Duplicates: {analysis.get('duplicates', 'n/a')}

    Columns Information:
    {_format_column_info(column_info)}

    Please provide a concise summary of the dataset, highlighting any potential issues, trends, or insights that can be derived from the data.
    Your summary should be clear and actionable for stakeholders who may not have a technical background.
    Keep these points in mind while generating the summary:
    1. What type of dataset is this?
    2. Give a concise summary.
    3. Identify data quality issues.
    4. Recommend cleaning steps.
    5. Suggest useful analyses or visualizations.
    """

    try:
        client = get_client()
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        return getattr(response, "text", "Unable to generate summary.")
    except Exception as exc:
        return f"Unable to generate AI summary: {exc}"


def clean_data(df, instructions):
    print(f"User instructions: {instructions}")
    print(f"DataFrame shape before cleaning: {df.shape}")
    return df

