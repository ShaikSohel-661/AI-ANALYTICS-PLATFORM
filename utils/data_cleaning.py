import json
from utils.ai_models import generate_solution


# CLEANING OPERATIONS

def remove_duplicates(df):
    return df.drop_duplicates()


def drop_column(df, operation):
    column = operation["column"]

    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist.")

    return df.drop(columns=[column])


def rename_column(df, operation):
    old_name = operation["old_name"]
    new_name = operation["new_name"]

    if old_name not in df.columns:
        raise ValueError(f"Column '{old_name}' does not exist.")

    return df.rename(columns={old_name: new_name})


def fill_missing(df, operation):
    column = operation["column"]
    method = operation["method"]
    value = operation["value"]

    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist.")

    if method == "value":
        df[column] = df[column].fillna(value)

    elif method == "mean":
        df[column] = df[column].fillna(df[column].mean())

    elif method == "median":
        df[column] = df[column].fillna(df[column].median())

    elif method == "mode":
        df[column] = df[column].fillna(df[column].mode()[0])

    else:
        raise ValueError(f"Unknown fill method: {method}")

    return df


def drop_missing(df, operation):
    column = operation.get("column")

    if column:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist.")

        return df.dropna(subset=[column])

    return df.dropna()


def filter_rows(df, operation):

    column = operation["column"]
    condition = operation["condition"]
    value = operation.get("value")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist.")

    if condition == "greater_than":
        return df[df[column] <= value]

    elif condition == "less_than":
        return df[df[column] >= value]

    elif condition == "equal_to":
        return df[df[column] != value]

    elif condition == "not_equal":
        return df[df[column] == value]

    elif condition == "greater_than_or_equal":
        return df[df[column] < value]

    elif condition == "less_than_or_equal":
        return df[df[column] > value]

    else:
        raise ValueError(f"Unknown condition: {condition}")


def replace_values(df, operation):

    column = operation["column"]
    old_value = operation["old_value"]
    new_value = operation["new_value"]

    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist.")

    df[column] = df[column].replace(old_value, new_value)

    return df


# OPERATION DISPATCHER

def apply_operation(df, operation):

    action = operation["action"]

    if action == "remove_duplicates":
        return remove_duplicates(df)

    elif action == "drop_column":
        return drop_column(df, operation)

    elif action == "rename_column":
        return rename_column(df, operation)

    elif action == "fill_missing":
        return fill_missing(df, operation)

    elif action == "drop_missing":
        return drop_missing(df, operation)

    elif action == "filter_rows":
        return filter_rows(df, operation)

    elif action == "replace_values":
        return replace_values(df, operation)

    else:
        raise ValueError(f"Unknown cleaning action: {action}")

def clean_data(df, instructions):
    columns = df.columns.tolist()
    prompt = f"""
    You are a data cleaning assistant.
    Your job is to interpret the user's cleaning instruction
    and convert it into a structured cleaning plan.
    User's instruction: {instructions}
    The dataset has the following columns: {columns}
    Return ONLY in JSON format.

    Convert the user's instruction into one or more structured
    cleaning operations.

     Return ONLY valid JSON.

    Available operations:

    1. remove_duplicates

    Example:
        {{
            "action": "remove_duplicates"
        }}

    2. drop_column

    Example:
        {{
            "action": "drop_column",
            "column": "CustomerName"
        }}

    3. rename_column

    Example:
        {{
            "action": "rename_column",
            "old_name": "CustomerName",
            "new_name": "Customer"
        }}

    4. fill_missing

    Methods available:
        - value
        - mean
        - median
        - mode

    Example:
        {{
            "action": "fill_missing",
            "column": "Age",
            "method": "median",
            "value": null
        }}

    5. drop_missing

    Example:
        {{
            "action": "drop_missing",
            "column": "Age"
        }}

    6. filter_rows

        Conditions available:
        - greater_than
        - less_than
        - equal_to
        - not_equal
        - greater_than_or_equal
        - less_than_or_equal
    Example:
        {{
            "action": "filter_rows",
            "column": "TotalPrice",
            "condition": "greater_than",
            "value": 1000
        }}

    7. replace_values

    Example:
        {{
            "action": "replace_values",
            "column": "Region",
            "old_value": "South",
            "new_value": "South India"
        }}

    Rules:

    - Only use columns that actually exist in the dataset.
    - Never invent a column.
    - Do not make assumptions about missing values.
    - If the user's instruction is ambiguous, return an error.
    - Return an object containing an "operations" list.

    Example response:

        {{
            "operations": [
                {{
                    "action": "remove_duplicates"
                }},
                {{
                    "action": "drop_column",
                    "column": "CustomerName"
                }}
            ]
        }}
    Return ONLY raw valid JSON.

    Do NOT use Markdown.
    Do NOT wrap the response in ```json or ```.
    Do NOT include explanations, comments, or any text before or after the JSON.
    The first character of your response must be {{ and the last character must be }}.

    """

    try:
        response_text = generate_solution(prompt)
        if response_text is None:
            raise ValueError("No response from AI model.")
    
        cleaning_plan = json.loads(response_text)

        for operation in cleaning_plan["operations"]:
            df = apply_operation(df, operation)

        return df

    except Exception as exc:
        print("Cleaning error:", exc)
        raise
        

