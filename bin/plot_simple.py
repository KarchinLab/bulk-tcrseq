#!/usr/bin/env python3

"""
Description: plotting simple clonality calculations on TCR repertoire

Authors: Domenick Braccia, Yuval Elhanaty
"""

## import packages
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import math

# initialize parser
parser = argparse.ArgumentParser(description='Plotting simple clonality calculations on TCR repertoire')
parser.add_argument('sample_table',
    metavar='sample_table',
    type=argparse.FileType('r'),
    help='metadata passed in through samples CSV file')
parser.add_argument('combined_csv', 
    metavar='combined_csv', 
    type=argparse.FileType('r'), 
    help='combined CSV file')
parser.add_argument('v_family_csv',
    metavar='v_family_csv',
    type=argparse.FileType('rb'),
    help='v_family usage data in CSV file')

args = parser.parse_args()

# Read in the combined CSV file with specified header
df = pd.read_csv(args.combined_csv, sep=',', header=0, 
                 names=['sample_id', 'patient_id', 'timepoint', 'origin', 'num_clones', 
                        'num_TCRs', 'simpson_index', 'simpson_index_corrected', 'clonality',
                        'num_in', 'num_out', 'num_stop', 'pct_prod', 'pct_out', 'pct_stop', 'pct_nonprod',
                        'cdr3_avg_len'])

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

# Read in sample metadata
meta = pd.read_csv(args.sample_table, sep=',', header=0, index_col=None,
                   names=['sample_id', 'file_path', 'patient_id', 'timepoint', 'origin'])
print('metadata looks like this: \n' )
print(meta.head())

# Read in v_family_csv file
v_family = pd.read_csv(args.v_family_csv, sep=',', header=0, index_col=None,
                       names=['patient_id', 'timepoint', 'origin', 'TCRBV01', 
                              'TCRBV02', 'TCRBV03', 'TCRBV04', 'TCRBV05', 'TCRBV06',
                              'TCRBV07', 'TCRBV08', 'TCRBV09', 'TCRBV10', 'TCRBV11',
                              'TCRBV12', 'TCRBV13', 'TCRBV14', 'TCRBV15', 'TCRBV16',
                              'TCRBV17', 'TCRBV18', 'TCRBV19', 'TCRBV20', 'TCRBV21',
                              'TCRBV22', 'TCRBV23', 'TCRBV24', 'TCRBV25', 'TCRBV26',
                              'TCRBV27', 'TCRBV28', 'TCRBV29', 'TCRBV30'])
v_family = v_family.sort_values(by=['patient_id', 'timepoint'])

# Loop through each patient and plot gene usage
# Calculate the number of rows and columns
N = len(v_family['patient_id'].unique())
rows = math.ceil(N / 2)
cols = 2

# Create a figure and axes for subplots
patients = v_family['patient_id'].unique()
fig, axes = plt.subplots(rows, cols, figsize=(12, rows*7), sharey=True)

for i, ax in enumerate(axes.flatten()):
    if i >= len(patients):
        ax.set_visible(False)
        continue
    
    pt = v_family[v_family['patient_id'] == patients[i]]
    pt['identity'] = pt['timepoint'].str.cat(pt['origin'], sep='_')
    
    # removing metadata columns and set new index
    pt_raw = pt.drop(['patient_id', 'timepoint', 'origin'], axis=1)
    pt_raw.set_index('identity', inplace=True)

    # calculate percentages for each gene from the row total
    pt_pct = pt_raw.apply(lambda row: row / row.sum(), axis=1)

    #### ================ PLOTTING ================ ####

    # Create a color palette
    colors = sns.cubehelix_palette(n_colors=len(pt_pct.columns),
                               start = 1.75, rot = 1, reverse=True)
    cmap1 = LinearSegmentedColormap.from_list("my_colormap", colors)

    # Plot stacked bar chart for current patient
    pt_pct.plot(ax=ax, kind='bar', stacked=True, colormap=cmap1, 
                edgecolor='white')
    ax.set_title(str(patients[i]))
    ax.set_ylabel('Portion of TCRs')
    ax.get_legend().set_visible(False)

    # Align x-axis plots
    ax.set_xticks(range(len(pt_pct.index)))
    ax.set_xticklabels(pt_pct.index, fontsize=12,
                       rotation=0, ha='center')
    ax.set_xlabel('')  # Remove x-label 'identity'

# Add a common title for the whole figure
fig.suptitle('V Family Usage for All Patients', fontsize=24)

# Create a common legend outside the loop
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='center left', bbox_to_anchor=(1.0, 0.5))

# Adjust spacing between subplots
plt.tight_layout()
fig.subplots_adjust(top=0.96)

plt.savefig('v_family_usage.png')
plt.close()