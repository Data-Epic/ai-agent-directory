"""
Idempotent ETL Job Script.

Name: Arowosegbe Victor Iyanuoluwa
Email: iyanuvicky@gmail.com
Github: https://github.com/Iyanuvicky22/Projects
"""

from pathlib import Path
from utils.utils import read_data, clean_data, transform_data
from models import load_data
import pandas as pd
from utils.utils import fetch_latest_csv_from_s3




def run_basic_etl() -> pd.DataFrame:
    """
    Basic ETL Job.
    Returns:
        pd.DataFrame: Ai tools data to run etl job on.
    """
    # download latest file from s3
    scraped_data_source = fetch_latest_csv_from_s3()

    scraped_df = read_data(scraped_data_source)

    clean_scraped_df = clean_data(scraped_df)

    trans_scraped_df = transform_data(clean_scraped_df)

    # load_data(trans_scraped_df)

    return trans_scraped_df


if __name__ == "__main__":
    run_basic_etl()
