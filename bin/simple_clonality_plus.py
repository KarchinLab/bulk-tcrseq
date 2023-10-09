#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 22:38:35 2023

@author: elhanaty
"""

from scipy.stats import entropy
import numpy as np

#%% repertoire statistics
clones = np.array([10, 6, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1 ]) #clones sizes. could be values of a dict or column in a table. 

clone_entropy = entropy(clones, base=2)
num_clones = len(clones)
num_TCRs = sum(clones)
clonality = 1 - clone_entropy / np.log2(num_clones)
simpson_index = sum(clones**2)/(num_TCRs**2)
simpson_index_corrected = sum(clones*(clones-1))/(num_TCRs*(num_TCRs-1))

#%% overlap measures
# I suggest using dictoneries for the clones sizes internally like this

clone_table1 = {'CASSQAGVSNERLFF' : 10,
 'CASGDRTSSAETLYF' : 7,
 'CASSLRTGVQNTLYF' : 5,
 'CASSDWGGSQNTLYF' : 4,
 'CASSLGGEGNTEVFF' : 4,
 'CTCSAEGHSGNTLYF' : 3,
 'CAWSLPGGYAEQFF' : 2,
 'CAWSETVNQDTQYF' : 2,
 'CASSAWGGEDTQYF' : 1,
 'CASSIMRLAETLYF' : 1,
 'CGARIGNTGQLYF' : 1,
 'CASRGQNERLFF' : 1}


clone_table2 = {'CASSQAGVSNERLFF' : 12,
 'CASSLGGQIYAEQFF' : 6,
 'CASSLRTGVQNTLYF' : 4,
 'CASSDWGGSQNTLYF' : 3,
 'CASSLGGEGNTEVFF' : 1,
 'CTCSVGQGTNTEVFF' : 2,
 'CTCSAEGHSGNTLYF' : 2,
 'CAWSLPGGYAEQFF' : 1,
 'CAWSETVNQDTQYF' : 1,
 'CASSAWGGEDTQYF' : 1,
 'CAWSLPGDERLFF' : 1}

clones1 = np.array(list(clone_table1.values()))

num_clones1 = len(clones1)
num_TCRs1 = sum(clones1)
simpson_index1 = sum(clones1**2)/(num_TCRs1**2) #these are the same expressions from before, should be functions
simpson_index_corrected1 = sum(clones1*(clones1-1))/(num_TCRs1*(num_TCRs1-1))

clones2 = np.array(list(clone_table2.values()))

num_clones2 = len(clones2)
num_TCRs2 = sum(clones2)
simpson_index2 = sum(clones2**2)/(num_TCRs2**2)
simpson_index_corrected2 = sum(clones2*(clones2-1))/(num_TCRs2*(num_TCRs2-1))

all_clones = clone_table1.keys() | clone_table2.keys()
shared_clones = clone_table1.keys() & clone_table2.keys()

jaccard_overlap = len(shared_clones) / len(all_clones)

raw_overlap =  2*sum([clone_table1[x]*clone_table2[x] for x in shared_clones])/(num_TCRs1*num_TCRs2)
morisita_overlap = raw_overlap/((simpson_index_corrected1 + simpson_index_corrected2))
morisita_horn_overlap = raw_overlap/((simpson_index1 + simpson_index2))