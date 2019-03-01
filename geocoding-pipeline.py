"""
geocoding-pipeline

Usage:
    geocoding-pipeline.py review <input_directory>
    geocoding-pipeline.py geocode <input_directory>
    geocoding-pipeline.py -h | --help
    geocoding-pipeline.py --version

Options:
    -h, --help                    show this screen
    --version:                    show the version number

"""


import pandas as pd
import os
import glob
import sys
from docopt import docopt
import review_tables
import geocode_tables


def main():
    args = docopt(__doc__, version='0.1.0')

    if args['review'] and args['<input_directory>']:
        print('Review addresses for errors')
        review_tables.main()

    elif args['geocode'] and args['<input_directory>']:
        print('Geocode all the addresses in tables found in ' + str(args['<input_directory>']))
        geocode_tables.main()



if __name__ == '__main__':
    sys.exit(main())
