import os 
import sys 
import pandas as pd 
import json
import matplotlib.pyplot as plt
import numpy as np


ver = 'r202'
file_name = sys.argv[1]
parent = file_name.split('/')[1][:-11]
xls = pd.ExcelFile(file_name)
taxons = [x[:-4] for x in xls.sheet_names]

# init rej_hists
rej_hists = []
for i in range(len(taxons)):
    rej_hists.append([])

# load threshod_dict
threshold_dict = json.load(open('rejection-threshold-'+'r202/'+parent+".json"))

# append confience distance to rejection thresholds to the right place 
for taxon in taxons:
    b_sheet = taxon + '-b-p'
    b_df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
    for index, row in b_df.iterrows():
        pred = row['prediction']
        p_i = taxons.index(pred)
        rej_hists[p_i].append(row['max'] - threshold_dict[pred])

print(rej_hists)
# plot histogtams
bin_width = 0.01
for taxon in taxons:
    i = taxons.index(taxon)
    plt.figure(i)
    # plt.hist(rej_hists[i], bins=np.arange(min(rej_hists[i]), max(rej_hists[i]) \
    #     + bin_width, bin_width))
    plt.hist(rej_hists[i], bins=100, density=True)
    plt.title(parent+'-'+taxon+' with rejection threshold: '+str(threshold_dict[taxon]))
    plt.savefig('outputs-'+ver+'/'+parent+'-'+taxon+'-hist.png')


    
        

        


