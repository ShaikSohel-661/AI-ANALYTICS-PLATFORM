import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(page_title="Data Visualization", page_icon="📈", layout="wide")

st.title("📊 Data Visualization")

if "cleaned_df" not in st.session_state:
    st.error("No dataset found. Please upload and clean a dataset first.")
    st.stop()
df = st.session_state.cleaned_df


st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])

st.subheader("Dataset Preview")
st.dataframe(df.head())

col1, col2 = st.columns([1, 3])

with col1:
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Pie Chart"],
        index=None,
        placeholder="Select a chart"
    )
    if chart_type is "Bar Chart":
        x_axis = st.selectbox(
            "Select X-axis",
            df.columns,
            index=None,
            placeholder="Select a column"
        )

        y_axis = st.selectbox(
            "Select Y-axis",
            df.columns,
            index=None,
            placeholder="Select a column"
        )

        aggregation = st.selectbox(
            "Select Aggregation",
            ["Sum", "Mean", "Count"],
            index=None,
            placeholder="Select aggregation"
        )

        generate_chart = st.button("Generate Chart")

    elif chart_type == "Line Chart":

        x_axis = st.selectbox(
            "Select X-axis",
            df.columns,
            index=None,
            placeholder="Select a column"
        )

        y_axis = st.selectbox(
            "Select Y-axis",
            df.columns,
            index=None,
            placeholder="Select a column"
        )

        aggregation = st.selectbox(
            "Select Aggregation",
            ["Sum", "Mean", "Count"],
            index=None,
            placeholder="Select aggregation"
        )

        generate_chart = st.button("Generate Chart")


    # 
    # SCATTER PLOT

    elif chart_type == "Scatter Plot":

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns

        x_axis = st.selectbox(
            "Select X-axis",
            numeric_columns,
            index=None,
            placeholder="Select numeric column"
        )

        y_axis = st.selectbox(
            "Select Y-axis",
            numeric_columns,
            index=None,
            placeholder="Select numeric column"
        )

        generate_chart = st.button("Generate Chart")


    # HISTOGRAM

    elif chart_type == "Histogram":

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns

        column = st.selectbox(
            "Select Column",
            numeric_columns,
            index=None,
            placeholder="Select numeric column"
        )

        bins = st.slider(
            "Number of Bins",
            min_value=5,
            max_value=50,
            value=20
        )

        generate_chart = st.button("Generate Chart")


    
    # PIE CHART

    elif chart_type == "Pie Chart":

        category_column = st.selectbox(
            "Select Category",
            df.columns,
            index=None,
            placeholder="Select category column"
        )

        value_column = st.selectbox(
            "Select Value",
            df.columns,
            index=None,
            placeholder="Select value column"
        )

        aggregation = st.selectbox(
            "Select Aggregation",
            ["Sum", "Mean", "Count"],
            index=None,
            placeholder="Select aggregation"
        )

        generate_chart = st.button("Generate Chart")
    

    with col2:
        if chart_type == "Bar Chart":
            if generate_chart:

                if x_axis and y_axis and aggregation:

                    if aggregation == "Sum":
                        chart_data = df.groupby(x_axis)[y_axis].sum()

                    elif aggregation == "Mean":
                        chart_data = df.groupby(x_axis)[y_axis].mean()

                    elif aggregation == "Count":
                        chart_data = df.groupby(x_axis)[y_axis].count()

                    st.subheader(
                        f"{aggregation} of {y_axis} by {x_axis}"
                    )

                    st.bar_chart(chart_data)

                else:
                    st.warning("Please select all chart options.")


        elif chart_type == "Line Chart":

            if generate_chart:

                if x_axis and y_axis and aggregation:

                    if aggregation == "Sum":
                        chart_data = df.groupby(x_axis)[y_axis].sum()

                    elif aggregation == "Mean":
                        chart_data = df.groupby(x_axis)[y_axis].mean()

                    elif aggregation == "Count":
                        chart_data = df.groupby(x_axis)[y_axis].count()

                    st.subheader(
                        f"{aggregation} of {y_axis} by {x_axis}"
                    )

                    st.line_chart(chart_data)

                else:
                    st.warning("Please select all chart options.")


        elif chart_type == "Scatter Plot":

            if generate_chart:

                if x_axis and y_axis:

                    st.subheader(
                        f"{y_axis} vs {x_axis}"
                    )

                    st.scatter_chart(
                        df,
                        x=x_axis,
                        y=y_axis
                    )

                else:
                    st.warning("Please select both X and Y columns.")


        elif chart_type == "Histogram":

            if generate_chart:

                if column:

                    st.subheader(
                        f"Distribution of {column}"
                    )

                    fig, ax = plt.subplots()

                    ax.hist(
                        df[column].dropna(),
                        bins=bins
                    )

                    ax.set_xlabel(column)
                    ax.set_ylabel("Frequency")

                    st.pyplot(fig)

                else:
                    st.warning("Please select a column.")


        elif chart_type == "Pie Chart":

            if generate_chart:

                if category_column and value_column and aggregation:

                    if aggregation == "Sum":
                        chart_data = df.groupby(
                            category_column
                        )[value_column].sum()

                    elif aggregation == "Mean":
                        chart_data = df.groupby(
                            category_column
                        )[value_column].mean()

                    elif aggregation == "Count":
                        chart_data = df.groupby(
                            category_column
                        )[value_column].count()

                    st.subheader(
                        f"{aggregation} of {value_column} by {category_column}"
                    )

                    fig, ax = plt.subplots()

                    ax.pie(
                        chart_data.values,
                        labels=chart_data.index,
                        autopct="%1.1f%%"
                    )

                    st.pyplot(fig)

                else:
                    st.warning("Please select all chart options.")

            