'''
verify_results.py

A module that takes all of the geocoded results and gives the user the option to
fix records that have a low match score.  Some records with a match score over 90
but less than 100 may have geocoded to the incorrect location.
'''

import os
import numpy as np
import pandas as pd
import glob

def main(directory_to_verify):
    print("Begin reviewing records..." + "\n" \
            "For each record in " + str(directory_to_verify) + ", you have the option to either " + "\n" \
            "accept the geocode match [a], enter a valid lat / long [l], or remove the record [r]." + "\n")
    os.chdir(directory_to_verify)
    os.chdir("..")

    final_results_directory = os.path.join(os.getcwd(), 'Final_Output')
    verify_records(directory_to_verify, final_results_directory)

def verify_records(directory_to_verify, final_results_directory):
    # Give user the option to accept the geocoded match, enter a verified lat / long
    # or remove the record
    unverified_tables = glob.glob(directory_to_verify + "\\*.xlsx", recursive=False)
    for table in unverified_tables:
        file_path = table
        file_name = file_path.split(sep='\\')
        file_root = file_name[-1]

        output_file_name = file_root.replace('Geocode', 'Results')

        df = pd.read_excel(table)

        # For all of the records with a null match score, set the match score to 0
        df_null_match = df[pd.isna(df['Score'])]
        if len(df_null_match) > 0:
            for index, row in df_null_match.iterrows():
                df.loc[[index], ['Score']] = 0.0

        # Load all records with a score less than 100.0 into a separate data frame
        df_to_review = df[df['Score'] < 100.0]

        if len(df_to_review) > 0:
            for index, row in df_to_review.iterrows():
                record_with_errors = str(df_to_review.loc[index, 'Company_Name']) + ", " + str(df_to_review.loc[index, 'Address']) \
                                    + ", " + str(df_to_review.loc[index, 'City']) + ", " + str(df_to_review.loc[index, 'State']) \
                                    + ", " + str(df_to_review.loc[index, 'ZIP_Code'])
                match_statement = "Matched with: " + "\n" \
                                    + str(df_to_review.loc[index, 'MatchAddress']) + " with a score of: " + str(df_to_review.loc[index, 'Score'])
                user_review_choices = input(record_with_errors + ": " + "\n" + match_statement + "\n" \
                                            + "Would you like to accept the existing match [a]," \
                                            " valid lat / long [l] or remove the record [r]?" \
                                            "\n ")
                if user_review_choices == "a":
                    print("Match accepted \n")
                    continue
                elif user_review_choices == "l":
                    new_coordinates = input("Enter a new pair of decimal degree coordinates (latitude, longitude): ")
                    new_latitude = new_coordinates.split(",")[0]
                    new_longitude = new_coordinates.split(",")[1]
                    df.loc[[index], ['Latitude']] = new_latitude
                    df.loc[[index], ['Longitude']] = new_longitude
                    print(df.loc[[index]])
                    print("Updated coordinates \n")
                elif user_review_choices == "r":
                    df = df.drop(index=index)
                    print("Removed the record from the Data Frame \n")
                else:
                    print("Invalid choice! You must choose to enter a new address [a]," \
                    " valid lat / long coordinates [l] or remove the record [r]." \
                    " This record will be removed by default. \n")

        # When the review step is finished, drop all of the unnecessary fields
        df.drop(['INID', 'INADDR', 'INZONE', 'MatchAddress', 'Zone', 'Score', 'XCoord', 'YCoord', 'Geocoder'], axis=1, inplace=True)
        print('Dropped unnecessary columns...\n')

        # When finished export the data into a final results folder
        df.to_excel(os.path.join(final_results_directory, output_file_name), sheet_name="Sheet1")
        print('Exported results to: ' + str(output_file_name))
