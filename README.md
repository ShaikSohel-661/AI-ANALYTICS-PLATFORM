# INGLYTICS

INGLYTICS is a Streamlit application I'm building to make basic data analysis easier using AI.

Users can upload a CSV or Excel file, inspect the dataset, get an AI-generated summary, clean the data using natural language instructions, and visualize the data.

## Features

* Upload CSV and Excel datasets
* View dataset overview such as rows, columns, missing values, duplicates, and memory usage
* Analyze individual columns
* Generate a summary of the dataset using AI
* Clean data using natural language instructions
* Create basic data visualizations
* Keep the cleaned data available while moving between pages

For data cleaning, the user's instruction is first converted by the AI into a structured cleaning operation. The actual changes are then performed using Pandas.

For example:

```text
Fill missing Promotion values with "No Promotion"
```

The application currently supports operations such as:

* Filling missing values
* Removing duplicates
* Dropping columns
* Renaming columns
* Filtering rows
* Replacing values

## AI Models

The project currently uses Gemini as the primary AI model and Mistral as a fallback.

If Gemini fails or is temporarily unavailable, the request is sent to Mistral instead. I added this mainly because API limits and temporary model availability were causing requests to fail during development.

## Data Visualization

The visualization page currently supports:

* Bar charts
* Line charts
* Scatter plots
* Histograms
* Pie charts

The page uses the latest version of the dataset, so if the user cleans the data first, the cleaned data is visualized.

## Tech Stack

* Python
* Streamlit
* Pandas
* Matplotlib
* Google Gemini API
* Mistral API

## Project Structure

```text
AI-ANALYTICS-PLATFORM/
├── app.py
├── pages/
│   └── visualization.py
├── utils/
│   ├── ai_models.py
│   ├── ai_summary.py
│   ├── col_analysis.py
│   ├── data_analysis.py
│   ├── data_cleaning.py
│   └── data_loader.py
├── requirements.txt
└── README.md
```

## What's Next

I'm still working on the project. Some features I plan to add are:

* Ask questions about the dataset using natural language
* AI-assisted visualization
* More visualization options and filters
* Export analysis reports
* Automatic dashboards

## Run Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Add your Gemini and Mistral API keys to a `.env` file:

```text
GOOGLE_API_KEY=your_api_key
MISTRAL_API_KEY=your_api_key
```

Then run:

```bash
streamlit run app.py
```
