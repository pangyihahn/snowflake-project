import os
from dotenv import load_dotenv
import snowflake.connector

# 1. Load the variables from your .env file
load_dotenv()

def test_connection():
    try:
        # 2. Establish connection using the .env variables
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        
        # 3. Create a cursor and run a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()
        
        print(f"✅ Success! Connected to Snowflake.")
        print(f"Snowflake Version: {version[0]}")
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    test_connection()