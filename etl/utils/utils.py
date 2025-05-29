"""
Utils function for ETL Job.

Name: Arowosegbe Victor Iyanuoluwa
Email: iyanuvicky@gmail.com
Github: https://github.com/Iyanuvicky22/Projects
"""
from pathlib import Path
import os
from datetime import datetime
from utils.logger_config import logger
import pandas as pd


def read_data(source_path: str) -> pd.DataFrame:
    """

    Args:
        source_path (str): Data Path

    Raises:
        ValueError: Raises error for unsupported data type.

    Returns:
        dataframe: Pandas Dataframe.
    """

    try:
        ext = Path(source_path).suffix
        if ext == ".csv":
            return pd.read_csv(source_path)
        elif ext == ".json":
            return pd.read_json(source_path)
        elif ext == ".parquet":
            return pd.read_parquet(source_path)
        logger.info("Data successfully read!")
    except Exception as e:
        logger.error(
            "Error raised at data loading. Unsupported file format! Use csv, json or parquet: %s",
            e,
            exc_info=True,
        )


def remove_hashtags(tags):
    """
    Method to clean tags column from "https://aitoolsdirectory.com/"
    Args:
        tags (Series): Column to be cleaned

    Returns:
        Series: Cleaned column.
    """
    try:
        if isinstance(tags, list):
            clean = [tag for tag in tags if "#" not in tag]
        elif isinstance(tags, str):
            clean = [tags] if "#" not in tags else []
        else:
            clean = []
        clean = ",".join(clean)

        if len(clean) < 4:
            clean = clean.upper()
        else:
            clean = clean.lower().capitalize()
    except Exception as e:
        logger.error("Error Raised at tags column cleaning:  %s", e, exc_info=True)
    return clean


def clean_data(df):
    """
    Custom function to clean scraped/manual ai_tools dataset
    Args:
        df (pd.DataFrame): Scraped/manually created ai_tools dataset.

    Returns:
        pd.DataFrame: Cleaned ai_tools dataset.
    """
    try:
        df = df.drop(columns=[col for col in ["pricing", "page"] if col in df.columns])
        new_df = df.dropna()
        new_df = new_df.reset_index(drop=True)

        if "tags" in df.columns:
            new_df["tags"] = new_df["tags"].apply(remove_hashtags)
        else:
            pass

        logger.info(
            "Columns dropped and null values dropped.",
            extra={
                "Cols dropped": ["pricing", "page"],
                "Null Values Dropped": len(df) - len(new_df),
            },
        )
        logger.info("Tags Column Successfully cleaned.")
        logger.info("Data successfully cleaned!")
    except Exception as e:
        logger.error("Error Raised at full cleaning process: %s", e, exc_info=True)
    return new_df


def get_created_at(filepath: str) -> str:
    """
    Extracting file creation date
    Args:
        filepath (str): filepath

    Returns:
        str: creation time in strings
    """
    try:
        created_timestamp = os.path.getctime(filepath)
        created_date = datetime.fromtimestamp(created_timestamp)
    except Exception as e:
        logger.error(f"Error Raised: {e}!", exc_info=True)
    return created_date.strftime("%Y-%M-%d")


def transform_data(df: pd.DataFrame, source=None) -> pd.DataFrame:
    """
    Custom function to transform any scraped and cleaned ai_tools dataset.
    Args:
        df (pd.DataFrame): Clean ai_tools dataset

    Returns:
        pd.DataFrame: Transformed ai_tools dataset
    """
    try:
        # created_day = get_created_at(scraped_data_source)
        if "source" in df.columns:
            if df["source"] is not None:
                pass
            else:
                df["source"] = source
        else:
            df["source"] = source

        if "created_at" in df.columns:
            if df["created_at"] is not None:
                pass
            else:
                df["created_at"] = None
        else:
            df["created_at"] = None
        if "updated_at" in df.columns:
            if df["updated_at"] is not None:
                pass
            else:
                df["updated_at"] = None
        else:
            df["updated_at"] = None

        if "trending" not in df.columns:
            df["trending"] = None
        else:
            df["trending"] = df['trending'].apply(
                lambda x: False if x == "Low" else True
                )
        df["trending"] = df["trending"].notna().astype(bool)

        trans_df = df.rename(columns={"url": "homepage_url", "tags": "category"})

        trans_df["created_at"] = pd.to_datetime(
            trans_df["created_at"], format="%Y-%M-%d", errors="coerce"
        )
        trans_df["updated_at"] = pd.to_datetime(
            trans_df["updated_at"], format="%Y-%M-%d", errors="coerce"
        )

        logger.info("Data successfully transformed!")
    except Exception as e:
        logger.error("Error Raised at transformation: %s", e, exc_info=True)
    return trans_df


def merging_dfs(new_df, existing_df) -> pd.DataFrame:
    """
    Merging DFs to extract unique ai_tools
    Returns:
        pd.DataFrame: Merged DF with unique Ai tools
    """
    try:
        merged_df = pd.merge(new_df, existing_df, how="outer")
        merged_df.drop_duplicates(subset="name", inplace=True)
        merged_df = merged_df.reset_index(drop=True)
        logger.info("Seed DF and Scraped DF successfully merged!")
    except Exception as e:
        logger.error("Error merging DFs: %s", e, exc_info=True)
    return merged_df
