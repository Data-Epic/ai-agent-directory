"""
Name: Arowosegbe Victor Iyanuoluwa
Email: iyanuvicky@gmail.com
Github: https://github.com/Iyanuvicky22/Projects
"""

import pandas as pd
from pathlib import Path

source_path = ""


def read_data(source_path):
    # Detect format and read
    ext = Path(source_path).suffix
    if ext == ".csv":
        return pd.read_csv(source_path)
    elif ext == ".json":
        return pd.read_json(source_path)
    elif ext == ".parquet":
        return pd.read_parquet(source_path)
    else:
        raise ValueError("Unsupported format")


def needs_transformation(df):
    # Add your logic here (e.g., missing columns, data types)
    return some_condition


def transform_data(df):
    # e.g., normalize URLs, fill NAs, reformat columns
    return transformed_df


def fetch_existing_records(conn):
    return pd.read_sql("SELECT name, homepage_url, email, phone FROM agents", conn)


def delta_check(new_df, existing_df):
    # Merge and check for differences
    merged = new_df.merge(
        existing_df, on=["name", "homepage_url"], how="left", suffixes=("", "_existing")
    )
    changed = merged[
        (merged["email"] != merged["email_existing"])
        | (merged["phone"] != merged["phone_existing"])
    ]
    return changed[new_df.columns]  # Only updated/new rows


def upsert_records(conn, df):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO agents (name, homepage_url, email, phone)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(name, homepage_url)
            DO UPDATE SET email=excluded.email, phone=excluded.phone
        """,
            (row["name"], row["homepage_url"], row["email"], row["phone"]),
        )
    conn.commit()


def etl_job(source_path):
    df = read_data(source_path)

    if needs_transformation(df):
        df = transform_data(df)

    with engine.connect("agents.db") as conn:
        existing_df = fetch_existing_records(conn)
        delta_df = delta_check(df, existing_df)

        if not delta_df.empty:
            upsert_records(conn, delta_df)
            print(f"Upserted {len(delta_df)} records.")
        else:
            print("No changes detected. Idempotent run.")


etl_job("agents.csv")
