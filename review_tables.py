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
    if os.path.isdir(os.path.join(os.getcwd(), 'Geocoding_Results')):
        pass
    else:
        os.mkdir('Geocoding_Results')

    facilities_to_geocode = os.path.join(os.getcwd(), 'Facilities_to_Geocode')
    geocoding_results = os.path.join(os.getcwd(), 'Geocoding_Results')
    prep_excel_files(input_directory, facilities_to_geocode, geocoding_results)


# For each Excel file in <input_directory>, do the following:
def prep_excel_files(input_directory, directory_to_geocode, results_directory):
    print("Prepping Excel files")
    # Load the input Excel file into a pandas data frame
    original_excel_files = glob.glob(input_directory + "\\*.xlsx", recursive=False)
    for original_excel_file in original_excel_files:
        print(original_excel_file)
        output_excel_name = input("Choose an output name for this Excel file to feed into the geocoder: ")
        print("\n")
        df = pd.read_excel(original_excel_file)
        # Rename all of the column headers to replace spaces with underscores
        df.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
        # Create an 'ID' column in the data frame that we need for the geocoder
        df.insert(0, 'ID', range(1, 1 + len(df)))
        # Assign all records a latitude and longitude of 0.0 so that we can
        # insert known values and geocoded values later
        df['Latitude'] = 0.0
        df['Longitude'] = 0.0

        # Identify potential problem records
        # Find records where the 'Address' column is blank
        df_blanks = df[pd.isna(df['Address'])]
        if len(df_blanks) > 0:
            print(original_excel_file)
            print(df_blanks[['Company_Name', 'Address', 'City', 'State', 'ZIP_Code']])
            print('\n')

        # Find records where the 'Address' column doesn't have a number
        df_potential_no_number = df[pd.notna(df['Address'])]
        df_address_without_number = df_potential_no_number[df_potential_no_number.apply(lambda x: any(char.isdigit() for char in x['Address']) == False, axis=1)]

        # Combine df_blanks and df_address_without_number
        df_with_errors = pd.concat([df_blanks, df_address_without_number])

        # For each problem record, return the original address, city and zip code, then
        # give the user the option to input a valid address, set of
        # known longitude / latitude coordinates, or remove the record
        if len(df_with_errors) > 0:
            for index, row in df_with_errors.iterrows():
                record_with_errors = str(df_with_errors.loc[index, 'Company_Name']) + ", " + str(df_with_errors.loc[index, 'Address']) \
                                    + ", " + str(df_with_errors.loc[index, 'City']) + ", " + str(df_with_errors.loc[index, 'State']) \
                                    + ", " + str(df_with_errors.loc[index, 'ZIP_Code'])
                user_review_choices = input("Would you like to enter a new address [a]," \
                                            " valid lat / long [l] or remove the record [r] for" \
                                            "\n " + record_with_errors + ": ")
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
                    df = df.drop(index=index)
                    print("Removed the record from the Data Frame")
                else:
                    print("Invalid choice! You must choose to enter a new address [a]," \
                    " valid lat / long coordinates [l] or remove the record [r]." \
                    " This record will be removed by default.")

        # Export the data frame to a new Excel file that will feed into the geocoder
        # For records in the dataframe with no lat long, export to an Excel in the
        # directory to geocode
        df_with_no_latlong = df[df['Latitude'] == 0.0]
        if len(df_with_no_latlong) > 0:
            geocode_file_name = output_excel_name + "_to_geocode.xlsx"
            df_with_no_latlong.to_excel(os.path.join(directory_to_geocode, geocode_file_name), sheet_name="Sheet1", index=False)
            print("Exported " + str(geocode_file_name) + " to " + str(directory_to_geocode))
            print("\n")

        # For records in the dataframe with a valid lat long, export to an Excel in the
        # results direcotry
        df_with_latlong = df[df['Latitude'] != 0.0]
        if len(df_with_latlong) > 0:
            latlong_file_name = output_excel_name + "_latlong.xlsx"
            df_with_latlong.to_excel(os.path.join(results_directory, latlong_file_name), sheet_name="Sheet1", index=False)
            print("Exported " + str(latlong_file_name) + " to " + str(results_directory))
            print("\n")
