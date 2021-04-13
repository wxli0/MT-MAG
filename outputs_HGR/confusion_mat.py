import os 
import sys
import pandas as pd 

result_path = "HGR-prediction-full-path.csv"
results =  pd.read_csv(result_path, index_col=0, header=0, dtype = str)
print(results)

rank = 'phylum'
total_dist = {}
rej_dist = {}
incorrect_dist = {}
for index, row in results.iterrows():
    print(row)
    if row['Genus (reference)'] == 'Unassigned':
        continue
    taxon = row[rank[0].upper()+rank[1:]+ ' (reference)']
    if taxon in total_dist:
        total_dist[taxon] += 1
    else:
        total_dist[taxon] = 1
    if str(row['genus']) == 'nan' or 'reject' in str(row['genus']):
        print("adding to rej_dist")
        if taxon in rej_dist:
            rej_dist[taxon]  += 1
        else:
            rej_dist[taxon] = 1
    elif str(row['genus']) != 'g__'+str(row['Genus (reference)']):
        print("adding to incorrect_dist")
        if taxon in incorrect_dist:
            incorrect_dist[taxon] += 1
        else:
            incorrect_dist[taxon] = 1

        # print(row['Phylum (reference)'], row['Class (reference)'], row['Order (reference)'], row['Family (reference)'], row['Genus (reference)'])
    
print(total_dist)
print(rej_dist)
print(incorrect_dist)