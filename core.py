import os
import duckdb
import sqlglot
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

def get_snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE')
    )

def get_downloaded_tables(data_dir="data"):
    if not os.path.exists(data_dir):
        return []
    return [f.replace(".parquet", "").upper() for f in os.listdir(data_dir) if f.endswith(".parquet")]

def transpile_query(sf_sql):
    return sqlglot.transpile(sf_sql, read="snowflake", write="duckdb")[0]

def run_local(duck_sql, parquet_path, table_name):
    db = duckdb.connect(database=':memory:')
    try:
        db.execute(f"CREATE VIEW {table_name} AS SELECT * FROM read_parquet('{parquet_path}')")
        return db.execute(duck_sql).df()
    finally:
        db.close()