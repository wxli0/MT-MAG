import os
import pandas as pd 


def find_single_child(path, ranks, dir, suffix = ""):
    """
    Find exiting single child taxons in a classification result file
    
    :param path: path of the classification result file
    :type path: str
    :param ranks: list of ranks in the classification result file
    :type ranks: List(str)
    :param dir: directory of training dataset
    :type dir: str
    :param suffix: suffix of the subdirectories in the dir
    :type suffix: str
    """
    single_child_taxons = []
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)
    all_taxons = []
    for rank in ranks:
        all_taxons.extend(list(df[rank]))
    all_taxons = list(set(all_taxons))
    for taxon in all_taxons:
        taxon = str(taxon)
        if 'uncertain' in taxon or taxon == 'nan':
            continue
        children = os.listdir(os.path.join(dir,taxon+suffix))
        if len(children) == 1:
            single_child_taxons.append(taxon)
    return single_child_taxons

find_single_child('~/MT-MAG/outputs-GTDB-r202-archive3/GTDB-r202-prediction-full-path.csv', \
    ['domain', 'phylum', 'class', 'order', 'family', 'genus'], '/mnt/sda/MLDSP-samples-r202')

