import streamlit as st
import pandas as pd


# Set page title
st.set_page_config(page_title="CSV Viewer App")

st.title("CSV Viewer App")

# Create sidebar for file upload
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Display table if file is uploaded
if uploaded_file is not None:
    ## allow multiple file uploads
    df = pd.read_csv(uploaded_file).reset_index(drop=True)
    df = df.filter(regex='^(?!Unnamed)')

    # Remove null rows
    df = df.dropna(how='all')

    # Iterate over columns to determine data types
    column_types = df.dtypes.to_dict()
    for column_name, column_type in column_types.items():
        if column_type == "object":
            temp_date_column = pd.to_datetime(df[column_name], errors='coerce')
            if temp_date_column.notnull().sum() > 0.8 * len(df[column_name]):
                df[column_name ] = temp_date_column
                column_types[column_name] = "datetime64[ns]"
                continue
            else:
                try:
                    df[column_name] = pd.to_numeric(df[column_name], errors='raise')
                    column_types[column_name] = "datetime64[ns]"
                except ValueError:
                    df[column_name] = df[column_name].astype(str)
                    column_types[column_name] = "string"

    # Display search box for filtering rows by text input
    search_term = st.sidebar.text_input("Search", "")
    if search_term:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, regex=False)).any(axis=1)]

    # Display table with filtered data
    st.dataframe(df, width=None)

    # Display this option as a collapsible section
    with st.sidebar.expander("Modify Column Types"):
        # for each column, if the inferred data type is not correct, display a dropdown menu to select the correct data type
        column_types = df.dtypes.to_dict()
        for column_name, column_type in column_types.items():
            if column_type == "object":
                st.selectbox(column_name, ["string", "number", "datetime"], index=0)

    # For each column, display a collapsible section that shows statistics for that column
    with st.expander("View Summary Statistics"):
        column_types = df.dtypes.to_dict()
        print (column_types)
        for column_name, column_type in column_types.items():
            st.write(df[column_name].describe())
    