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

# define functions
def plot_timecourse(df, x_col, y_col, patient_col):
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
    plt.title(f'{y_col} over {x_col}')

# initialize parser
parser = argparse.ArgumentParser(description='Plotting simple clonality calculations on TCR repertoire')
parser.add_argument('combined_csv', 
    metavar='combined_csv', 
    type=argparse.FileType('r'), 
    help='combined CSV file')

args = parser.parse_args()

# Read in the combined CSV file with specified header
combined_df = pd.read_csv(args.combined_csv, 
                          sep=',', header=0, 
                          names=['sample_id', 'patient_id', 'timepoint', 'origin', 'num_clones', 
                                 'num_TCRs', 'simpson_index', 'simpson_index_corrected', 'clonality',
                                 'num_in', 'num_out', 'num_stop', 'pct_prod', 'pct_out', 'pct_stop', 'pct_nonprod'])

## initializing the subplot
fig, axs = plt.subplots(ncols=4, nrows=1,
                        figsize=(15,5))
fig.tight_layout(pad=2)

## num_clones boxplot
sns.boxplot(data=combined_df, x='timepoint', y='num_clones', showfliers=False, ax=axs[0], color='white')
sns.stripplot(data=combined_df, x='timepoint', y='num_clones',color='black', size=4, ax=axs[0])
axs[0].set(xlabel='', ylabel='')
axs[0].set_title('Num Clones')

## clonality boxplot
sns.boxplot(data=combined_df, x='timepoint', y='clonality', showfliers=False, ax=axs[1], color='white')
sns.stripplot(data=combined_df, x='timepoint', y='clonality',color='black', size=4, ax=axs[1])
axs[1].set(xlabel='', ylabel='')
axs[1].set_title('Clonality')

## simpson_index_corrected boxplot
sns.boxplot(data=combined_df, x='timepoint', y='simpson_index_corrected', showfliers=False, ax=axs[2], color='white')
sns.stripplot(data=combined_df, x='timepoint', y='simpson_index_corrected',color='black', size=4, ax=axs[2])
axs[2].set(xlabel='', ylabel='')
axs[2].set_title('Simpson Index Corrected')

## pct_prod boxplot
sns.boxplot(data=combined_df, x='timepoint', y='pct_prod', showfliers=False, ax=axs[3], color='white')
sns.stripplot(data=combined_df, x='timepoint', y='pct_prod',color='black', size=4, ax=axs[3])
axs[3].set(xlabel='', ylabel='')
axs[3].set_title('Percent Productive')

## save the plot
plt.savefig('clonality.png')

##### TCR PRODUCTIVITY PLOTS #####

# Define the variables to plot
variables = ['num_clones', 'clonality', 'simpson_index_corrected', 'pct_prod']

# Create a figure object for the grid of plots
fig = plt.figure(figsize=(15, 5))
fig.tight_layout(pad=2)

# Iterate over the variables and plot each one in a separate axis
for i, var in enumerate(variables):
    # Create a new axis object for the current plot
    ax = fig.add_subplot(1, 4, i+1)

    # Plot the current variable in the corresponding axis
    plot_timecourse(combined_df, 'timepoint', var, 'patient_id')

    # Add a title to the axis
    ax.set(ylabel='', xlabel='')
    ax.set_title(var)

# Add a common y-axis label to the leftmost plot
fig.text(0.05, 0.5, '', va='center', rotation='vertical', fontsize=14)

## save the plot
plt.savefig('timecourse.png')