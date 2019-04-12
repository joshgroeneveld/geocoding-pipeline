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

# Import the geocoding toolbox here so that it gets imported before switching directories
arcpy.ImportToolbox('geocoding-toolbox-pro-python-3/TableGeocoder/AGRC Geocode Tools.tbx')

def main(directory_to_geocode):
    print("Begin geocoding records")

    os.chdir(directory_to_geocode)
    os.chdir("..")

    geocoding_results = os.path.join(os.getcwd(), 'Geocoding_Results')
    # Create a directory to store the final Excel files
    if os.path.isdir(os.path.join(os.getcwd(), 'Final_Output')):
        pass
    else:
        os.mkdir('Final_Output')
    final_output_directory = os.path.join(os.getcwd(), 'Final_Output')
    geocode_tables(directory_to_geocode, final_output_directory, geocoding_results)

# For each table in <directory_to_geocode>, send all records through the geocoder
def geocode_tables(directory_to_geocode, final_output_directory, geocoding_results_directory):
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
                os.rename(file, file_root + "_geocoding_results.csv")

# Load the input Excel files and the output geocoded CSVs into separate Pandas data frames

# Join the Excel data frame and the CSV data frame based on the input ID

# Output the joined data frame to a new Excel file in the final output directory
