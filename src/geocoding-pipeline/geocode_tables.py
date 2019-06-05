'''
geocode_tables.py

A module that takes all of the reviewed tables, sends them through the geocoder,
joins the geocode outputs with the original inputs and exports to a new Excel file.
'''

import os
import arcpy
from api_key import API_KEY
import glob
import pandas as pd
import numpy as np
import shutil

# Import the geocoding toolbox here so that it gets imported before switching directories
arcpy.ImportToolbox('geocoding-toolbox-pro-python-3/TableGeocoder/AGRC Geocode Tools.tbx')

def main(directory_to_geocode):
    print("Begin geocoding records")

    os.chdir(directory_to_geocode)
    os.chdir("..")

    geocoding_results = os.path.join(os.getcwd(), 'Geocoding_Results')
    # Create a directory to store the unverified and final Excel files
    if os.path.isdir(os.path.join(os.getcwd(), 'Unverified_Results')):
        pass
    else:
        os.mkdir('Unverified_Results')
    if os.path.isdir(os.path.join(os.getcwd(), 'Final_Output')):
        pass
    else:
        os.mkdir('Final_Output')
    unverified_results_directory = os.path.join(os.getcwd(), 'Unverified_Results')
    final_results_directory = os.path.join(os.getcwd(), 'Final_Output')
    geocode_tables(directory_to_geocode, unverified_results_directory, geocoding_results)
    join_geocode_results_with_inputs(directory_to_geocode, geocoding_results, unverified_results_directory)
    prompt_user_to_verify_results(unverified_results_directory, final_results_directory)

# For each table in <directory_to_geocode>, send all records through the geocoder
def geocode_tables(directory_to_geocode, unverified_results_directory, geocoding_results_directory):
    print("Geocoding tables...")

    api_key = API_KEY
    # Set variables to send table through the geocoder
    excel_files_to_geocode = glob.glob(directory_to_geocode + "\\*.xlsx", recursive=False)
    for excel_file in excel_files_to_geocode:
        print("Geocoding addresses in " + excel_file)
        file_to_geocode = excel_file + "\\Sheet1$"
        # Setup the geocoding results file output file name
        file_path = excel_file
        file_name = file_path.split(sep='\\')
        file_root = file_name[-1].split(sep='_to_')[0]
        # results_file_name = os.path.join(geocoding_results_directory, file_root + "_geocoding_results.xlsx")
        # Run the geocoder
        arcpy.GeocodeTable.GeocodeTable(api_key,
                                        file_to_geocode,
                                        "ID",
                                        "Address",
                                        "ZIP_Code",
                                        "Address points and road centerlines (default)",
                                        'GCS WGS 1984',
                                        geocoding_results_directory)

        # Rename the output CSVs to match the input Excel files
        for file in os.listdir(geocoding_results_directory):
            if file.startswith("GeocodeResults_"):
                os.rename(os.path.join(geocoding_results_directory, file), os.path.join(geocoding_results_directory, file_root + "_geocoding_results.csv"))

    # Join geocoding results with the original tables, concatentate the results with the known lat / long
    # locations identified in the review step
def join_geocode_results_with_inputs(directory_to_geocode, geocoding_results_directory, unverified_results_directory):
    print("Joining inputs and outputs...")
    # Load the input Excel files and the output geocoded CSVs into separate Pandas data frames
    input_excel_files = glob.glob(directory_to_geocode + "\\*.xlsx", recursive=False)
    for input_excel_file in input_excel_files:
        excel_df = pd.read_excel(input_excel_file)
        file_path = input_excel_file
        file_name = file_path.split(sep='\\')
        file_root = file_name[-1].split(sep='_to_')[0]
        results_csv = glob.glob(geocoding_results_directory + "\\" + file_root + "*.csv", recursive=False)[0]
        csv_df = pd.read_csv(results_csv)

        # Join the Excel data frame and the CSV data frame based on the input ID
        merge_df = pd.merge(excel_df, csv_df, how='inner', left_on='ID', right_on='INID')
        merge_df['Latitude'] = merge_df['YCoord']
        merge_df['Longitude'] = merge_df['XCoord']

        # If there is a file with known lat / long locations identified in the review step,
        # load them into another pandas dataframe and concatentate with the dataframe merged above
        output_file_dir = unverified_results_directory
        output_file_name = file_root + "_Geocode.xlsx"

        # Verify that the output file name has 31 or fewer characters.  Some Excel files with
        # file names longer than 31 characters can cause problems.
        if len(output_file_name[:-5]) > 31:
            print("Currently exporting: " + output_file_name + ", but there are too many characters..." + "\n")
            print("Your current output file name is: " + len(output_file_name[:-5]) + " characters" + "\n")
            output_file_name = input("Choose a file name with 31 or fewer characters: ") + ".xlsx"

        results_latlong = glob.glob(geocoding_results_directory + "\\" + file_root + "_latlong.xlsx", recursive=False)
        if len(results_latlong) == 1:
            latlong_df = pd.read_excel(results_latlong[0])
            latlong_df.assign(**{'INID': np.nan, 'INADDR': np.nan, 'INZONE': np.nan, 'MatchAddress': np.nan, 'Score': np.nan, 'XCoord': np.nan, 'YCoord': np.nan, 'Geocoder': np.nan})
            concat_df = pd.concat([merge_df, latlong_df], sort=False)
            concat_df.to_excel(os.path.join(output_file_dir, output_file_name), sheet_name="Sheet1")
            print("Exported: " + str(output_file_name))

        elif len(results_latlong) == 0:
            merge_df.to_excel(os.path.join(output_file_dir, output_file_name), sheet_name="Sheet1")
            print("Exported: " + str(output_file_name))

        else:
            print("There are more than two lat / long results with the same name...")
    print("Completed joining inputs and outputs!")


def prompt_user_to_verify_results(unverified_directory, final_results_directory):
    verify_choice = input("Do you want to review results with a low match score? [y / n]")
    if verify_choice == 'y':
        print('The unverified results are located in ' + str(unverified_directory) + '. \n' \
            'Please run python geocoding-pipeline.py verify ' + str(unverified_directory))
    elif verify_choice == 'n':
        print('Moving unverified results into the final output directory...')
        unverified_results = glob.glob(unverified_directory + '\\*.xlsx', recursive=False)
        for file in unverified_results:
            shutil.copy2(file, final_results_directory, follow_symlinks=True)
        print('Copied files into the final results directory.  Geocoding complete!')
