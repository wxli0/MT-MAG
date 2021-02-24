import sys

import pandas as pd 
import sys
import operator
import platform

# for GTDB-Tk classification

base_path = "/Users/wanxinli/Desktop/project/MLDSP-desktop/data/DS_10283_3009/" # run locally
if platform.platform()[:5] == 'Linux':
    base_path = "/home/w328li/MLDSP-desktop/data/DS_10283_3009/"
    

results_table = pd.read_excel(base_path+"paper_results.xlsx", sheet_name = "Table S5", skiprows = [0,1])
results_table = results_table[['MAG', 'GTDB_Tk_classification']]
taxon_num = 7
print(results_table)
taxon_names = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
for index, row in results_table.iterrows():
    taxon_path = row['GTDB_Tk_classification'].split(';')
    taxon_path += ['NA'] * (taxon_num-len(taxon_path))
    results_table.at[index, 'GTDB_Tk_classification'] = ";".join(taxon_path)
    
for i in range(len(taxon_names)):
    taxon  = taxon_names[i]
    results_table[taxon] = results_table.apply(lambda row: row.GTDB_Tk_classification.split(";")[i], axis=1)
results_table = results_table.set_index('MAG')
del results_table['GTDB_Tk_classification']

results_table.to_csv(base_path+'GTDB-Tk_classification.csv')
