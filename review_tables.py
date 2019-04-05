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
        # print(df.head())

        # Identify potential problem records
        # Find records where the 'Address' column is blank
        df_blanks = df[pd.isna(df['Address'])]
        if len(df_blanks) > 0:
            print(original_excel_file)
            print(df_blanks[['Company_Name', 'Address', 'City', 'State', 'ZIP_Code']])
            print('\n')

        # Find records where the 'Address' column doesn't have a number

        # For each problem record, return the original address, city and zip code, then
        # give the user the option to input a valid address, set of
        # known longitude / latitude coordinates, or remove the record
            for index, row in df_blanks.iterrows():
                # print(index)
                user_review_choices = input("Would you like to enter a new address [a]," \
                                            " valid lat / long [l] or remove the record [r] for" \
                                            "\n " + str(df_blanks.loc[index, 'Company_Name']) + ": ")
                if user_review_choices == "a":
                    new_address = input("Enter a new address: ")
                    df.loc[[index], ['Address']] = new_address
                    print(df.loc[[index]])
                    print("Updated address")
                elif user_review_choices == "l":
                    new_coordinates = input("Enter a new pair of decimal degree coordinates (latitude, longitude): ")
                    new_latitude = new_coordinates.split(",")[0]
                    new_longitude = new_coordinates.split(",")[1]
                    df.loc[[index], ['Latitude']] = new_latitude
                    df.loc[[index], ['Longitude']] = new_longitude
                    print(df.loc[[index]])
                    print("Updated coordinates")
                elif user_review_choices == "r":
                    df.drop(index=index)
                    print("Removed the record from the Data Frame")

# Export the data frame to a new Excel file that will feed into the geocoder
