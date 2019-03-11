'''
review_tables.py

A module that reviews all of the input Excel files to check for easy-to-catch errors
'''

import os
import shutil
import glob
import pandas as pd

def main(input_directory):
    print("Begin reviewing records")
    # Make a new directory called 'Facilities_to_Geocode' to store the clean,
    # ready to geocode, inputs
    os.chdir(input_directory)
    os.chdir("..")
    if os.path.isdir(os.path.join(os.getcwd(), 'Facilities_to_Geocode')):
        pass
    else:
        os.mkdir('Facilities_to_Geocode')

    facilities_to_geocode = os.path.join(os.getcwd(), 'Facilities_to_Geocode')
    prep_excel_files(input_directory, facilities_to_geocode)


# For each Excel file in <input_directory>, do the following:
def prep_excel_files(input_directory, output_directory):
    print("Prepping Excel files")
    # Load the input Excel file into a pandas data frame
    original_excel_files = glob.glob(input_directory + "\\*.xlsx", recursive=False)
    for original_excel_file in original_excel_files:
        df = pd.read_excel(original_excel_file)
        # Rename all of the column headers to replace spaces with underscores
        df.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
        print(df.head())

# Identify potential problem records

    # Find records where the 'Address' column is blank

    # Find records where the 'Address' column doesn't have a number

# For each problem record, return the original address, city and zip code, then
# give the user the option to input a valid address, set of
# known longitude / latitude coordinates, or remove the record

# Export the data frame to a new Excel file that will feed into the geocoder
