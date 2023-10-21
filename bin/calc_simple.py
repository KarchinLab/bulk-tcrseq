#!/usr/bin/env python3
"""
Description: this script calculates the clonality of a TCR repertoire

@author: Domenick Braccia
@contributor: elhanaty
"""

## import packages
import argparse
import pandas as pd
from scipy.stats import entropy
import numpy as np
from pathlib import Path
import csv
# import logging
# import sys

# print('-- ENTERED calc_clonality.py--')

# initialize parser
parser = argparse.ArgumentParser(description='Calculate clonality of a TCR repertoire')

# add arguments
parser.add_argument('-m', '--metadata', 
                    metavar='metadata', 
                    type=str, 
                    help='metadata passed in through samples CSV file')
parser.add_argument('-c', '--counts', 
                    metavar='counts', 
                    type=argparse.FileType('r'), 
                    help='counts file in TSV format')

args = parser.parse_args() 

## convert metadata to list
s = args.metadata
metadata = args.metadata[1:-1].split(', ')
# print('metadata looks like this: ' + str(metadata))

# Read in the counts file
counts = pd.read_csv(args.counts, sep='\t', header=0)
counts = counts.rename(columns={'count (templates/reads)': 'read_count', 'frequencyCount (%)': 'frequency'})
# print('counts columns: \n')
# print(counts.columns)

def calc_clonality(metadata, counts):
    """Calculate clonality of a TCR repertoire."""

    clone_counts = counts['read_count']
    clone_entropy = entropy(clone_counts, base=2)
    num_clones = len(clone_counts)
    num_TCRs = sum(clone_counts)
    clonality = 1 - clone_entropy / np.log2(num_clones)
    simpson_index = sum(clone_counts**2)/(num_TCRs**2)
    simpson_index_corrected = sum(clone_counts*(clone_counts-1))/(num_TCRs*(num_TCRs-1))

    # print('Number of clones: ' + str(num_clones))
    # print('Number of TCRs: ' + str(num_TCRs))
    # print('Simpson Index: ' + str(simpson_index))
    # print('Simpson Index Corrected: ' + str(simpson_index_corrected))
    # print('Clonality: ' + str(clonality))
    # print('\n')

    # write above values to csv file
    # print('--- Writing repertoire stats to file...')
    with open('simple_calc.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['sample_name', 'patient_id', 'timepoint', 'origin', 'num_clones', 'num_tcrs', 'simpson_index', 'simpson_index_corr', 'clonality'])
        writer.writerow([metadata[0], metadata[1], metadata[2], metadata[3], num_clones, num_TCRs, simpson_index, simpson_index_corrected, clonality])

calc_clonality(metadata, counts)