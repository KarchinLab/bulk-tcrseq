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

    ## first pass stats
    clone_counts = counts['read_count']
    clone_entropy = entropy(clone_counts, base=2)
    num_clones = len(clone_counts)
    num_TCRs = sum(clone_counts)
    clonality = 1 - clone_entropy / np.log2(num_clones)
    simpson_index = sum(clone_counts**2)/(num_TCRs**2)
    simpson_index_corrected = sum(clone_counts*(clone_counts-1))/(num_TCRs*(num_TCRs-1))

    ## tcr productivity stats
    clone_prod = counts['sequenceStatus']
    # print('clone_prod looks like this: ' + str(clone_prod))

    # count number of productive clones
    num_in = sum(clone_prod == 'In')
    num_out = sum(clone_prod == 'Out')
    num_stop = sum(clone_prod == 'Stop')
    pct_prod = num_in / num_clones
    pct_out = num_out / num_clones
    pct_stop = num_stop / num_clones
    pct_nonprod = pct_out + pct_stop

    ## cdr3 info
    cdr3_len = counts['cdr3Length']

    # CDR3_dict = {}
    # for seq in counts['aminoAcid']:
    #     print('seq looks like this: ' + str(seq))
    #     if len(seq) == 0:
    #         continue
    #     else:
    #         if seq not in CDR3_dict:
    #             CDR3_dict[seq] = [counts['read_count'], counts['frequency'], counts['cdr3Length'], 
    #                               counts['vGeneName'], counts['dGeneName'], counts['jGeneName']]
    #         else:
    #             continue
    # print('CDR3_dict looks like this: ' + str(CDR3_dict))

    # calculate gene usage
    v_family = counts['vFamilyName'].value_counts(dropna=False)
    d_family = counts['dFamilyName'].value_counts(dropna=False)
    j_family = counts['jFamilyName'].value_counts(dropna=False)
    print('v_family looks like this: ' + str(v_family))
    print('d_family looks like this: ' + str(d_family))
    print('j_family looks like this: ' + str(j_family))

    v_genes = counts['vGeneName'].value_counts(dropna=False)
    d_genes = counts['dGeneName'].value_counts(dropna=False)
    j_genes = counts['jGeneName'].value_counts(dropna=False)
    print('v_genes looks like this: ' + str(v_genes))
    print('d_genes looks like this: ' + str(d_genes))
    print('j_genes looks like this: ' + str(j_genes))

    # write above values to csv file
    with open('simple_calc.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([metadata[0], metadata[1], metadata[2], metadata[3], 
                         num_clones, num_TCRs, simpson_index, simpson_index_corrected, clonality,
                         num_in, num_out, num_stop, pct_prod, pct_out, pct_stop, pct_nonprod,
                         cdr3_len])

calc_clonality(metadata, counts)