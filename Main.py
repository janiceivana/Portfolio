import sqlite3
import pandas as pd
import streamlit as st

# Load SQL file into SQLite
def load_database(sql_file):
    conn = sqlite3.connect(":memory:")  # use ":memory:" for temporary db
    cursor = conn.cursor()
    with open(sql_file, "r") as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    return conn

st.title("📊 SQL Database Viewer")

# Upload .sql file
uploaded_file = st.file_uploader("singapore_mrt.sql", type=["sql"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp.sql", "wb") as f:
        f.write(uploaded_file.read())

    conn = load_database("temp.sql")
    st.success("Database loaded successfully!")

    # Get all tables
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    table_names = tables["name"].tolist()

    option = st.selectbox("Select a table to view:", table_names)

    if option:
        df = pd.read_sql(f"SELECT * FROM {option};", conn)
        st.dataframe(df)
