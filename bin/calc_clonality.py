#!/usr/bin/env python3
"""
Description: this script calculates the clonality of a TCR repertoire

@author: Domenick Braccia
@contributor: elhanaty
"""

## import packages
import argparse
import logging
import csv
import sys
from scipy.stats import entropy
import numpy as np
from pathlib import Path

logger = logging.getLogger()
parser = argparse.ArgumentParser(description='Calculate clonality of a TCR repertoire')

def calc_clonality(metadata, counts):
    """Calculate clonality of a TCR repertoire."""

    # Read in the metadata file and counts file
    print('metadata head looks like this: ' + str(metadata.head()))
    print('counts head looks like this: ' + str(counts.head()))

    # Calculate clonality for each sample
    ## code here


    '''
    # Read in the metadata file
    with metadata.open(mode="r") as file_in:
        reader = csv.DictReader(file_in, delimiter=",")
        header = list(reader.fieldnames)
        #header.insert(1, "single_end")
        # See https://docs.python.org/3.9/library/csv.html#id3 to read up on `newline=""`.
        with file_out.open(mode="w", newline="") as out_handle:
            writer = csv.DictWriter(out_handle, header, delimiter=",")
            writer.writeheader()
    # Read in the counts file
    with counts.open(mode="r") as file_in:
        reader = csv.DictReader(file_in, delimiter=",")
        header = list(reader.fieldnames)
        #header.insert(1, "single_end")
        # See https://docs.python.org/3.9/library/csv.html#id3 to read up on `newline=""`.
        with file_out.open(mode="w", newline="") as out_handle:
            writer = csv.DictWriter(out_handle, header, delimiter=",")
            writer.writeheader()
    '''

def parse_args(argv=None):
    """Define and parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Calculate clonality of a TCR repertoire",
        epilog="Example: python calc_clonality.py -m metadata.csv -c counts.csv",
    )
    parser.add_argument(
        "metadata",
        metavar="metadata",
        type=Path,
        help="metadata file in CSV format",
    )
    parser.add_argument(
        "counts",
        metavar="counts",
        type=Path,
        help="counts file in TSV format",
    )

def main(argv=None):
    """Coordinate argument parsing and program execution."""
    args = parser.parse_args(argv)
    logging.basicConfig(level=args.log_level, format="[%(levelname)s] %(message)s")
    if not args.metadata.is_file():
        logger.error(f"The given input file {args.metadata} was not found!")
        sys.exit(2)
    args.file_out.parent.mkdir(parents=True, exist_ok=True)
    calc_clonality(args.metadata, args.counts)
    #print(args.metadata)
