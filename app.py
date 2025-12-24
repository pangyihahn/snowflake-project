import streamlit as st
import os
import pandas as pd
from core import transpile_query, run_local, get_snowflake_conn, get_downloaded_tables

st.set_page_config(page_title="Snowflake Transpiler", layout="wide", page_icon="❄️")

st.markdown("""
    <style>
    .stTextArea textarea { font-family: 'Source Code Pro', monospace; border-radius: 8px; }
    .stCodeBlock { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("❄️ Local Snowflake SQL Transpiler")

with st.sidebar:
    downloaded = get_downloaded_tables()
    selected_table = st.selectbox(
        "📂 Select Downloaded Table", 
        ["---"] + downloaded
    )
    
    st.divider()
    
    input_schema = st.text_input("Schema", value="TPCH_SF1")
    input_table = st.text_input("Table")
    
    if st.button("📥 Download New Table", width="stretch"):
        if not input_table:
            st.error("Please enter a table name.")
        else:
            with st.spinner(f"Downloading {input_table}..."):
                try:
                    conn = get_snowflake_conn()
                    df = pd.read_sql(f"SELECT * FROM {input_schema}.{input_table}", conn)
                    os.makedirs("data", exist_ok=True)
                    df.to_parquet(f"data/{input_table.lower()}.parquet")
                    st.toast(f"{input_table} downloaded!", icon="✅")
                    conn.close()
                    st.rerun() 
                except Exception as e:
                    st.error(f"Error: {e}")

active_table = selected_table if selected_table != "---" else input_table

if active_table:
    st.subheader(f"Workspace: {active_table}")
    
    sql_col, transpile_col = st.columns(2)

    with sql_col:
        sql_input = st.text_area(
            "Snowflake SQL", 
            height=220, 
            placeholder=f"SELECT * FROM {active_table} LIMIT 10"
        )

    duck_sql = ""
    if sql_input:
        try:
            duck_sql = transpile_query(sql_input)
        except Exception as e:
            duck_sql = f"-- Error: {e}"

    with transpile_col:
        st.markdown(f"<p style='font-size: 14px; margin-bottom: 5px;'>DuckDB SQL</p>", unsafe_allow_html=True)
        st.code(duck_sql, language="sql")

    if st.button("🚀 Run Local Execution", type="primary", width="stretch"):
        parquet_path = f"data/{active_table.lower()}.parquet"
        if not os.path.exists(parquet_path):
            st.warning(f"⚠️ No local data for '{active_table}'. Please download it first.")
        else:
            try:
                results = run_local(duck_sql, parquet_path, active_table)
                st.divider()
                st.subheader("📊 Results")
                st.dataframe(results, width="stretch", hide_index=True)
            except Exception as e:
                st.error(f"Execution Error: {e}")
else:
    st.info("💡 Please select a table from the sidebar or download a new one to begin.")