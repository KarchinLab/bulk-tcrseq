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
                                 'num_TCRs', 'simpson_index', 'simpson_index_corrected', 'clonality'])

## initializing the subplot
fig, axs = plt.subplots(ncols=3, nrows=1,
                        figsize=(10,5))
fig.tight_layout(pad=2)

## num_clones boxplot
sns.boxplot(data=combined_df, x='timepoint', y='num_clones', 
            showfliers=False, ax=axs[0], color='white')
sns.stripplot(data=combined_df, x='timepoint', y='num_clones',
                color='black', size=4, ax=axs[0])
axs[0].set(xlabel='', ylabel='')
axs[0].set_title('Num Clones')

## clonality boxplot
sns.boxplot(data=combined_df, x='timepoint', y='clonality', 
            showfliers=False, ax=axs[1], color='white')
sns.stripplot(data=combined_df, x='timepoint', y='clonality',
                color='black', size=4, ax=axs[1])
axs[1].set(xlabel='', ylabel='')
axs[1].set_title('Clonality')

## simpson_index_corrected boxplot
sns.boxplot(data=combined_df, x='timepoint', y='simpson_index_corrected', 
            showfliers=False, ax=axs[2], color='white')
sns.stripplot(data=combined_df, x='timepoint', y='simpson_index_corrected',
                color='black', size=4, ax=axs[2])
axs[2].set(xlabel='', ylabel='')
axs[2].set_title('Simpson Index Corrected')

## save the plot
plt.savefig('combined_plots.png')

##### NEXT PLOT #####

# fig, axs = plt.subplots(ncols=2,
#                         wspace=0.2,
#                         hspace=0.5,
#                         figsize=(10,10))

# ## num_TCRs boxplot
# sns.boxplot(data=combined_df, x='timepoint', y='num_TCRs', 
#             showfliers=False, ax=axs[0,1], color='timepoint')
# sns.stripplot(data=combined_df, x='timepoint', y='num_TCRs',
#                 color='black', size=4, ax=axs[0,1])
# axs[0,1].set_title('Num TCRs')


## create a boxplot comparing num_clones at each timepoint

# print('combined_df looks like this: \n')
# print(combined_df.head())

# # Create a figure with multiple subplots
# fig, axs = plt.subplots(ncols=4, figsize=(20, 5))

# # Create a box plot with data points overlaid for each variable
# sns.boxplot(data=combined_df, x='timepoint', y='num_clones', showfliers=False, ax=axs[0])
# sns.stripplot(data=combined_df, x='timepoint', y='num_clones', color='black', size=4, ax=axs[0])
# sns.boxplot(data=combined_df, x='timepoint', y='num_TCRs', showfliers=False, ax=axs[1])
# sns.stripplot(data=combined_df, x='timepoint', y='num_TCRs', color='black', size=4, ax=axs[1])
# sns.boxplot(data=combined_df, x='timepoint', y='clonality', showfliers=False, ax=axs[2])
# sns.stripplot(data=combined_df, x='timepoint', y='clonality', color='black', size=4, ax=axs[2])
# sns.boxplot(data=combined_df, x='timepoint', y='simpson_index_corrected', showfliers=False, ax=axs[3])
# sns.stripplot(data=combined_df, x='timepoint', y='simpson_index_corrected', color='black', size=4, ax=axs[3])

# # Set the title for each subplot
# axs[0].set_title('Num Clones')
# axs[1].set_title('Num TCRs')
# axs[2].set_title('Clonality')
# axs[3].set_title('Simpson Index Corrected')

# # Remove the y-axis label from each subplot
# axs[0].set(xlabel='', ylabel='')
# axs[1].set(xlabel='', ylabel='')
# axs[2].set(xlabel='', ylabel='')
# axs[3].set(xlabel='', ylabel='')

# # Remove the top and right spines from each subplot
# sns.despine(ax=axs[0], left=True, bottom=True)
# sns.despine(ax=axs[1], left=True, bottom=True)
# sns.despine(ax=axs[2], left=True, bottom=True)
# sns.despine(ax=axs[3], left=True, bottom=True)

# # Save each subplot as a separate PNG file
# plt.savefig('combined_plots.png', bbox_inches='tight')
