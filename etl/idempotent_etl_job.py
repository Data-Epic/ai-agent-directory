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

scraped_data_source = r"C:\Users\APIN PC\OneDrive\Documents\DS\DE_Inter\data_epic_capstone\etl\data\29-05-2025_ai_tools_scraped.json"


def run_basic_etl() -> pd.DataFrame:
    """
    Basic ETL Job.
    Returns:
        pd.DataFrame: Ai tools data to run etl job on.
    """
    scraped_df = read_data(scraped_data_source)

    clean_scraped_df = clean_data(scraped_df)

    trans_scraped_df = transform_data(clean_scraped_df)

    load_data(trans_scraped_df)

    return trans_scraped_df


if __name__ == "__main__":
    run_basic_etl()
