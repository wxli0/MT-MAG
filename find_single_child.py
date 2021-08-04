import os
import pandas as pd 


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
        children = os.listdir(dir+taxon+suffix)
        if len(children) == 1:
            single_child_taxons.append(taxon)
    return single_child_taxons

