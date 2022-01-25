"""
Checks incomplete entries in HGR/GTDB-prediction-full-path.csv.

No command line arguments are required. 
"""

import os
import pandas as pd


def check_invalid(data_dir, path):
    """
    Determines the single child genus and query instances with GTDB-tk classified \
        species not exist in training dataset, and single-child genera
    :param data_dir: training dataset directory
    :type data_dir: str
    :param path: MT-MAG and GTDB-tk result path
    :type path: str
    """
    
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)
    all_species = []
    for dir in os.listdir(data_dir):
        # single child for genus 
        if (data_dir == '/mnt/sda/DeepMicrobes-data/labeled_genome-r202/' and \
            dir.startswith('g__') and dir.endswith('_split_pruned') and dir != 'g__') \
            or (data_dir == '/mnt/sda/MLDSP-samples-r202/' and dir.startswith('g__') and dir != 'g__'):
            dir_path = data_dir + dir + '/'
            children = os.listdir(dir_path)
            all_species.extend(children)
                

    index_species_not_exist = []
    for index, row in df.iterrows():
        # ground-truth label does not exist in training dataset 
        if row['gtdb-tk-species'] == 's__':
            index_species_not_exist.append(index)
        elif row['gtdb-tk-species'] not in all_species and data_dir == '/mnt/sda/DeepMicrobes-data/labeled_genome-r202/':
            index_species_not_exist.append(index)
    return index_species_not_exist

print("========== checking invalid entries in HGR ===============")
HGR_path = './outputs-HGR-r202-archive1/HGR-r202-prediction-full-path.csv'
data_dir1 = '/mnt/sda/DeepMicrobes-data/labeled_genome-r202/'
index_species_not_exist1 = check_invalid(data_dir1, HGR_path)
print("index_species_not_exist1 length is:", len(index_species_not_exist1), index_species_not_exist1)
# print("single_child_genus1 length is:", len(single_child_genus1), single_child_genus1)
        
print("========== checking invalid entries in GTDB ===============")
MLDSP_path = './outputs-GTDB-r202-archive1/GTDB-r202-prediction-full-path.csv'
data_dir2 = '/mnt/sda/MLDSP-samples-r202/'
index_species_not_exist2 = check_invalid(data_dir2, MLDSP_path)
print("index_species_not_exist2 length is:", len(index_species_not_exist2), index_species_not_exist2)
# print("single_child_genus2 length is:", len(single_child_genus2), single_child_genus2)
