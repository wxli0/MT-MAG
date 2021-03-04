import sys
import pandas as pd
import math
import openpyxl
import json

# e.g. 
taxon = sys.argv[1]
rep_dict = json.load(open(sys.argv[2]))


MLDSP_pred_path = "outputs/MLDSP-prediction-full-path.csv"

taxons = ['domain', "phylum", "class", "order", "family", "genus", 'species']


MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
# print(MLDSP_df)
# print(math.isnan(MLDSP_df.loc['RUG518']['family']))
for index, row in MLDSP_df.iterrows():
    if row[taxon] in rep_dict:
        print("index is:", index)
        next_taxon= taxons[taxons.index(taxon)+1]
        MLDSP_df.at[index, next_taxon] = row[rep_dict[row[taxon]]]

print(MLDSP_df)

MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)
