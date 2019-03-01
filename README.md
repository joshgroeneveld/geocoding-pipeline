# geocoding-pipeline

This tool is a Python-based CLI to take input Excel files, geocode the records in those files against the AGRC geocoding API and return new Excel files with the original data and the geocoded location data.

This tool is based on the existing [AGRC geocoding toolbox](https://github.com/agrc/geocoding-toolbox), which is a Python 2 script compatible with ArcMap.  This script updates the AGRC geocoding toolbox to work with Python 3 and uses the `requests` library instead of `urllib`.

To use this tool (and any of the other AGRC API functions), you need to [sign up for a free API key on their website](https://developer.mapserv.utah.gov/AccountAccess).

## Inputs
- Directory of Excel files
- AGRC mapserv API key

## Steps
- Create a workspace directory to store reviewed input Excel files
- Create a geocoding output directory to store output CSVs from the AGRC API
- Create a final output directory to store Excel files that contain the original data in addition to the geocoded location data
- Review input Excel files for records that could cause problems, like records with a blank address
- After review, loop through each input Excel file and geocode all of the records
- Store the geocoded results in the geocode output directory and rename the output CSVs to match the input Excel files
- Load the input Excel files and the output geocoded CSVs into separate Pandas data frames
- Join the Excel data frame and the CSV data frame based on the input ID
- Output the joined data frame to a new Excel file in the final output directory

## CLI Options
<pre>
  <code>
    "geocoding-pipeline
    
    Usage:
      geocoding-pipeline.py review &ltinput_directory&gt
      geocoding-pipeline.py geocode &ltinput_directory&gt
      geocoding-pipeline.py -h | --help
      geocoding-pipeline.py --version

    Options:
    --help, -h:                   show this screen
    --version:                    show the version number
    "
  </code>
</pre>
