import os
import sys
import pandas as pd



def check_invalid(data_dir, path):
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)
    single_child_genus = []
    all_species = []
    for dir in os.listdir(data_dir):
        # single child for genus 
        if (data_dir == '/mnt/sda/DeepMicrobes-data/labeled_genome-r202/' and dir.startswith('g__') and dir.endswith('_split_pruned')) \
            or (data_dir == '/mnt/sda/MLDSP-samples-r202/' and dir.startswith('g__')):
            dir_path = data_dir + dir + '/'
            children = os.listdir(dir_path)
            if len(children) == 1:
                single_child_genus.append(dir[:-13])
            else:
                all_species.extend(children)

    index_species_not_exist = []
    index_genus_single_child = []
    for index, row in df.iterrows():
        # ground-truth label does not exist in training dataset 
        if row['gtdb-tk-species'] not in all_species:
            index_species_not_exist.append(index)
        # genus prediction with single child
        elif row['genus'] in single_child_genus or row['gtdb-tk-genus'] in single_child_genus:
            index_genus_single_child.append(index)
    return index_species_not_exist, index_genus_single_child

HGR_path = '~/BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv'
data_dir1 = '/mnt/sda/DeepMicrobes-data/labeled_genome-r202/'
index_species_not_exist1, index_genus_single_child1 = check_invalid(data_dir1, HGR_path)
print("index_species_not_exist1 length is:", len(index_species_not_exist1), index_species_not_exist1)
print("index_genus_single_child1 length is:", len(index_genus_single_child1), index_genus_single_child1)
        
MLDSP_path = '~/BlindKameris-new/outputs-r202/MLDSP-prediction-full-path.csv'
data_dir2 = '/mnt/sda/MLDSP-samples-r202/'
index_species_not_exist2, index_genus_single_child2 = check_invalid(data_dir2, MLDSP_path)
print("index_species_not_exist2 length is:", len(index_species_not_exist2), index_species_not_exist2)
print("index_genus_single_child2 length is:", len(index_genus_single_child2), index_genus_single_child2)
