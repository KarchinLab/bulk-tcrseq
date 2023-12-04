#!/usr/bin/env python3

"""
Description: plotting simple clonality calculations on TCR repertoire

Authors: Domenick Braccia, elhanaty
"""

## import packages
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

# initialize parser
parser = argparse.ArgumentParser(description='Plotting simple clonality calculations on TCR repertoire')
parser.add_argument('combined_csv', 
    metavar='combined_csv', 
    type=argparse.FileType('r'), 
    help='combined CSV file')
parser.add_argument('pickle_files', nargs='*',
    metavar='pickle_files',
    type=argparse.FileType('rb'),
    help='pickled gene usage data')

args = parser.parse_args()

# Read in the combined CSV file with specified header
df = pd.read_csv(args.combined_csv, sep=',', header=0, 
                 names=['sample_id', 'patient_id', 'timepoint', 'origin', 'num_clones', 
                        'num_TCRs', 'simpson_index', 'simpson_index_corrected', 'clonality',
                        'num_in', 'num_out', 'num_stop', 'pct_prod', 'pct_out', 'pct_stop', 'pct_nonprod',
                        'cdr3_avg_len'])

# Read in the pickled gene usage data
for file in args.pickle_files:
    # get name of file
    current_filename = os.path.splitext(os.path.basename(file.name))[0]

    # dynamically name the loaded data using filename
    globals()[current_filename] = pickle.load(file)
    print('loaded pickle file: ' + current_filename)

# global variables
print('global variables: \n' + str(globals().keys()))

# local variables
print('local variables: \n' + str(locals().keys()))

##### ==================================================================== #####
#
#           COMBINED BOX AND LINE TIMECOURSE PLOTS
#
##### ==================================================================== #####

## making a function to create combined plot

def plot_timecourse2(df, x_col, y_col, patient_col):
    # Create a list of colors for the scatter plot points
    colors = []
    for timepoint in df[x_col]:
        if timepoint == 'Base':
            colors.append('blue')
        elif timepoint == 'Post':
            colors.append('orange')

    # Create a scatter plot of the data with the specified colors
    plt.scatter(df[x_col], df[y_col], c=colors)

    # Find the indices of the Base timepoints
    base_indices = df[df[x_col] == 'Base'].index

    # Iterate over the Base timepoints and plot lines to the corresponding Post timepoints
    for base_idx in base_indices:
        # Get the x and y coordinates of the Base timepoint
        base_x, base_y = df.loc[base_idx, [x_col, y_col]]

        # Find the index of the corresponding Post timepoint (if it exists)
        post_idx = df[(df[patient_col] == df.loc[base_idx, patient_col]) & 
                      (df[x_col] == 'Post')].index
        if len(post_idx) > 0:
            # Get the x and y coordinates of the Post timepoint
            post_x, post_y = df.loc[post_idx[0], [x_col, y_col]]

            # Plot a line between the Base and Post timepoints
            plt.plot([base_x, post_x], [base_y, post_y], color='black')

    # Add labels and title to the plot
    plt.xlabel(x_col)
    plt.ylabel(y_col)

def plt_combined (df, x_col, y_col, patient_col='patient_id'):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    fig.tight_layout(pad=2)

    ## box/strip plots overlaid
    sns.boxplot(data=df, x=x_col, y=y_col, showfliers=False, ax=axs[0], color='white')
    sns.stripplot(data=df, x=x_col, y=y_col, color='black', size=4, ax=axs[0])
    axs[0].set(xlabel='', ylabel='')

    ## line plot using plot_timecourse2()
    plot_timecourse2(df, x_col=x_col, y_col=y_col, patient_col=patient_col)
    axs[1].set(ylabel='', xlabel='')

    ## figure adjustments
    fig.subplots_adjust(top=0.90)

    ## add title
    titles = {
        'num_clones': 'Number of unique T cell Clones',
        'clonality': 'Clonality of T cell repertoire',
        'simpson_index_corrected': 'Corrected Simpson index',
        'pct_prod': 'Percentage of productive TCR sequences',
        'cdr3_avg_len': 'Average Length of CDR3 sequences'
    }
    fig.suptitle(titles[y_col], fontsize=16)

    ## save the plot
    print('saving figure as: ' + y_col + '.png')
    plt.savefig(y_col + '.png')

## plot all the things
for var in ['num_clones', 'clonality', 'simpson_index_corrected', 'pct_prod', 'cdr3_avg_len']:
    plt_combined(df, x_col='timepoint', y_col=var, patient_col='patient_id')

##### ==================================================================== #####
#
#           GENE USAGE PLOTS
#
##### ==================================================================== #####

## import pickled data 

