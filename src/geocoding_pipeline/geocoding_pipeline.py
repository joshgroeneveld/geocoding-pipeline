"""
geocoding-pipeline

Usage:
    geocoding-pipeline.py review <input_directory>
    geocoding-pipeline.py geocode <input_directory>
    geocoding-pipeline.py verify <input_directory>
    geocoding-pipeline.py -h | --help
    geocoding-pipeline.py --version

Options:
    -h, --help                    show this screen
    --version:                    show the version number

Examples:
    geocoding-pipeline.py review <input_directory>  Loads each file in the input directory into a pandas dataframe
                                                    and gives the user options to fix problematic records before
                                                    exporting to a cleaned up file to send through the geocoder
    geocoding-pipeline.py geocode <input_directory> For each file in the input directory, send each record through
                                                    the geocoder and return geocoded records to a new file
    geocoding-pipeline.py verify <input_directory>  For each file in the input directory, review records with a match
                                                    score less than 100.  Export the results to a final output folder.

"""


import pandas as pd
import os
import glob
import sys
from docopt import docopt
import review_tables
import geocode_tables
import verify_results


def main():
    args = docopt(__doc__, version='0.3.0')

    if args['review'] and args['<input_directory>']:
        print('Review addresses for errors')
        review_tables.main(args['<input_directory>'])

    elif args['geocode'] and args['<input_directory>']:
        print('Geocode all the addresses in tables found in ' + str(args['<input_directory>']))
        geocode_tables.main(args['<input_directory>'])

    elif args['verify'] and args['<input_directory>']:
        print('Verify the low match scores in tables found in ' + str(args['<input_directory>']))
        verify_results.main(args['<input_directory>'])



if __name__ == '__main__':
    sys.exit(main())
