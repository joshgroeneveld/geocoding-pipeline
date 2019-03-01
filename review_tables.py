'''
review_tables.py

A module that reviews all of the input Excel files to check for easy-to-catch errors
'''

def main():
    print("Begin reviewing records")

# For each Excel file in <input_directory>, do the following:

# Make a new directory called 'Facilities_to_Geocode' to store the clean,
# ready to geocode, inputs

# Rename all of the column headers to replace spaces with underscores

# Identify potential problem records

    # Find records where the 'Address' column is blank

    # Find records where the 'Address' column doesn't have a number

# For each problem record, return the original address, city and zip code, then
# give the user the option to input a valid address, set of
# known longitude / latitude coordinates, or remove the record

# Export the data frame to a new Excel file that will feed into the geocoder
