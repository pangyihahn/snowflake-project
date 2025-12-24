# Local Snowflake SQL Transpiler

## Project Overview

This project is a tool to query Snowflake tables locally using **Parquet optimization**, **sqlglot transpilation**, and the **DuckDB engine**. It solves the challenges of high cloud latency and potential compute costs by providing a "Local-First" development environment. It allows engineers to iterate on complex logic instantly and for free before deploying to production.

## Features

- **Connects to Snowflake**: Securely connects to your Snowflake instance to pull live data for local development.
- **Save Tables as Parquet**: Converts Snowflake tables into optimized local Parquet files, significantly reducing data footprint while maintaining high performance.
- **Auto-Transpile SQL**: Automatically translates Snowflake-specific syntax (like `IFF`) into standard SQL compatible with the DuckDB engine for local testing.
- **Fast & Free Execution**: Provides sub-second query results using DuckDB, eliminating the need to spend Snowflake credits for logic testing and data analysis.
- **Local Scanner**: Automatically detects previously downloaded files so you can switch between datasets without re-downloading.

## Repository Contents

- `app.py`: The minimalist Streamlit user interface featuring a dynamic workspace.
- `core.py`: The core engine handling Snowflake connectivity, sqlglot transpilation, and DuckDB execution.

## Getting Started

### Step 1: Configure Environment Variables

Create a `.env` file in the root directory with your Snowflake credentials:
```plaintext
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_DATABASE=
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

### Step 4: Download and Query

1. Enter the **Schema** and **Table** in the sidebar and click **Download New Table**.
2. Once downloaded, select your table from the **Select Downloaded Table** dropdown.
3. Write your Snowflake SQL in the editor and click **Run Local Execution**.