import os
import pandas as pd 

path1 = "./outputs-r202/MLDSP-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus']
dir1 = '/mnt/sda/MLDSP-samples-r202/'
def find_single_child(path, ranks, dir, suffix = ""):
    single_child_taxons = []
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)
    all_taxons = []
    for rank in ranks:
        all_taxons.extend(list(df[rank]))
    all_taxons = list(set(all_taxons))
    for taxon in all_taxons:
        taxon = str(taxon)
        if 'reject' in taxon or taxon == 'nan':
            continue
        if len(os.listdir(dir+taxon+suffix)) == 1:
            single_child_taxons.append(taxon)
    return single_child_taxons


single_child_taxons= find_single_child(path1, ranks1, dir1)
print("single_child taxons for GTDB are:", single_child_taxons)


