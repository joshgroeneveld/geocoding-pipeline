import pytest
import pandas as pd
import os

from src.geocoding_pipeline import review_tables


# Does main geocoding-pipeline.py import other modules

def test_find_problem_records():
    # Review tables
    # Will records with a blank address get identified as potential problems
    # Will records without a number in the address get identified as a potential problem
    data_dir = os.path.join(os.getcwd(), 'tests\\data\\Original_Tables')
    os.chdir(data_dir)
    df_with_problem_records = pd.read_excel('Test Commercial Facilities.xlsx')
    df_identified_problems = review_tables.find_problem_records(df_with_problem_records)
    assert len(df_identified_problems) == 5

# For records with errors, check inputs to update records
# Will a new address be inserted into the data frame

# Will a new lat long be inserted into the data frame

# Will a record to be removed get dropped from the data frame

# Will a set of geocoding results merge with input data

# Will a merged df concatenate with a df of known lat / long locations

# Will user input to verify results move files appropriately

# Will records to be verified identify records with a low match score

# Once verification is complete, will the unnecessary columns get dropped
