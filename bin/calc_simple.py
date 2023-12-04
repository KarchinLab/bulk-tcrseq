#!/usr/bin/env python3
"""
Description: this script calculates the clonality of a TCR repertoire

@author: Domenick Braccia
@contributor: elhanaty
"""

## import packages
import argparse
import pandas as pd
import numpy as np
from scipy.stats import entropy
import numpy as np
from pathlib import Path
import csv
import pickle
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
    cdr3_lens = counts['cdr3Length']
    cdr3_avg_len = np.mean(cdr3_lens)

    # write above values to csv file
    with open('simple_stats.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([metadata[0], metadata[1], metadata[2], metadata[3], 
                         num_clones, num_TCRs, simpson_index, simpson_index_corrected, clonality,
                         num_in, num_out, num_stop, pct_prod, pct_out, pct_stop, pct_nonprod,
                         cdr3_avg_len])
        
    # store v_family gene usage in a dictionary
    v_family = counts['vFamilyName'].value_counts(dropna=False).to_dict()
    d_family = counts['dFamilyName'].value_counts(dropna=False).to_dict()
    j_family = counts['jFamilyName'].value_counts(dropna=False).to_dict()
    v_genes = counts['vGeneName'].value_counts(dropna=False).to_dict()
    d_genes = counts['dGeneName'].value_counts(dropna=False).to_dict()
    j_genes = counts['jGeneName'].value_counts(dropna=False).to_dict()

    # store dictionaries in a list and output to pickle file
    gene_usage = [v_family, d_family, j_family, v_genes, d_genes, j_genes]
    with open('gene_usage_' + str(metadata[1] + '_' + str(metadata[2] + '_' + str(metadata[3]))) + '.pkl', 'wb') as f:
        pickle.dump(gene_usage, f)

calc_clonality(metadata, counts)