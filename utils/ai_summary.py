from utils.ai_models import generate_solution

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

    response_text = generate_solution(prompt)

    if response_text is None:
        return "Unable to generate AI summary."

    return response_text


