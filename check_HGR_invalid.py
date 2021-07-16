import os
import sys
import pandas as pd

HGR_path = '~/BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv'
HGR_df =  pd.read_csv(HGR_path, index_col=0, header=0, dtype = str)

data_dir = '/mnt/sda/DeepMicrobes-data/labeled_genome-r202/'

single_child_genus = []
all_species = []
for dir in os.listdir(data_dir):
    # single child for genus 
    if dir.startswith('g__') and dir.endswith('_split_pruned'):
        dir_path = data_dir + dir + '/'
        children = os.listdir(dir_path)
        if len(children) == 1:
            single_child_genus.append(dir)
        else:
            all_species.extend(children)

print("single_child_genus is:", single_child_genus)
index_species_not_exist = []
index_genus_single_child = []
for index, row in HGR_df.iterrows():
    # ground-truth label does not exist in training dataset 
    if row['gtdb-tk-species'] not in all_species:
        index_species_not_exist.append(index)
    # genus prediction with single child
    elif row['genus'] in single_child_genus or row['gtdb-tk-genus'] in single_child_genus:
        index_genus_single_child.append(index)


print("index_species_not_exist length is:", len(index_species_not_exist), index_species_not_exist)
print("index_genus_single_child length is:", len(index_genus_single_child), index_genus_single_child)
        

