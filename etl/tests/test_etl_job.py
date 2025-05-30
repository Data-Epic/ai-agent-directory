import pytest
from idempotent_etl_job import (read_data, remove_hashtags, clean_data,
                                transform_data, merging_dfs, run_basic_etl)


"""
- test for duplicates.
- test for invalid rows.
- test for correct upserts.
"""

def test_read_data():
    pass
