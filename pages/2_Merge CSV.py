import streamlit as st
import pandas as pd

def join_on_mapped_columns(df1, df2, column_mappings):
    for left_col, right_col in column_mappings:
        if left_col in df1.columns and right_col in df2.columns:
            df1[left_col] = df1[left_col].astype(str)
            df2[right_col] = df2[right_col].astype(str)
            df1 = df1.merge(df2, left_on=left_col, right_on=right_col, how='inner')
            df1 = df1.drop(columns=[right_col])
        else:
            st.warning(f"Both columns {left_col} and {right_col} must be present in the respective files.")
    return df1

st.set_page_config(page_title="CSV Joiner", layout="wide")
st.title("CSV Joiner")

uploaded_files = st.file_uploader("Upload two CSV files", type="csv", accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 2:
    df1 = pd.read_csv(uploaded_files[0])
    df2 = pd.read_csv(uploaded_files[1])

    st.subheader("Select Columns to Map")
    column_mappings = []

    left_column = st.selectbox(f"Choose a column from the first file", options=df1.columns)
    right_column = st.selectbox(f"Choose a column from the second file", options=df2.columns)
    column_mappings.append((left_column, right_column))

    if column_mappings and all(mapping for mapping in column_mappings):
        st.subheader("Joined DataFrame")
        joined_df = join_on_mapped_columns(df1, df2, column_mappings)
        st.write(joined_df)
    else:
        st.warning("Please select columns to map.")
else:
    st.warning("Please upload exactly two CSV files to proceed.")
