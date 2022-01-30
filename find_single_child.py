"""
Post-process classification results for single-child classifications 
:param sys.argv[1]: data type. Data type for this task.
:type sys.argv[1]: str
:param sys.argv[2]: base path. base path of the training and testing sets.
:type sys.argv[2]: str
:params sys.argv[3]: all ranks of the tasks. 
:type sys.argv[3]: List[str]
"""

import math
import openpyxl
import os
import sys
import pandas as pd 


def find_single_child(data_type, ranks, base_path, suffix = ""):
    """
    Find exiting single child taxons in a classification result file
    
    :param data_type: data type of this task
    :type data_type: str
    :param ranks: list of ranks in the classification result file
    :type ranks: List(str)
    :param base_path: base path of training dataset
    :type base_path: str
    :param suffix: suffix of the subdirectories in the base path
    :type suffix: str
    """
    single_child_taxons = []
    ranks = ranks[:-1]
    path = os.path.join(os.path.join("outputs-"+data_type, data_type+"-full-path.csv"))
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)
    all_taxons = []
    for rank in ranks:
        all_taxons.extend(list(df[rank]))
    all_taxons = list(set(all_taxons))
    for taxon in all_taxons:
        taxon = str(taxon)
        if 'uncertain' in taxon or taxon == 'nan':
            continue
        children = os.listdir(os.path.join(base_path,taxon+suffix))
        if len(children) == 1:
            single_child_taxons.append(taxon)
    return single_child_taxons


def update_single_child(single_child, data_type):
    """
    Update single child taxa output files by max score
    If the max score is uncertain for an instance, update the prediction to uncertain
    :param single_child: single child taxa
    :type single_child: List[str]
    :param data_type: data type of this task
    :type data_type: str
    """
    output_dir = "outputs-"+data_type
    for child in single_child:
        file = os.path.join(output_dir, child+".xlsx")
        sheet = child+"_pred-t-p"
        df = pd.read_excel(file, index_col=0, header=0, sheet_name=sheet)
        rejection_f = []
        max_new = []
        neg_exists = False
        for index, row in df.iterrows():
            max_new.append(1/(1+math.exp(-row['max'])))
            if float(row['max']) < 0:
                neg_exists = True
                print(index, row['max'])
                rejection_f.append(row['prediction']+'(uncertain)')
            else:
                rejection_f.append(row['prediction'])

        del df['max']
        df['max'] = max_new
        
        if neg_exists:
            if 'rejection-f' in df.columns:
                del df['rejection-f']
            df['rejection-f'] = rejection_f

        wb = openpyxl.load_workbook(file)
        del wb[sheet]

        mode = 'w'
        if len(wb.sheetnames) != 0:
            wb.save(file)
            mode = 'a'

        with pd.ExcelWriter(file, engine="openpyxl", mode=mode) as writer:  
            df.to_excel(writer, sheet_name = sheet, index=True)
            writer.save()
        os.system("python3 add_pred.py " + file + " " + data_type)


data_type = sys.argv[1]
base_path = sys.argv[2]
ranks = sys.argv[3]

single_child_taxa = find_single_child(data_type, ranks, base_path)
update_single_child(single_child_taxa, data_type)

# # HGR_single_child = find_single_child('~/MT-MAG/outputs-HGR-r202-archive3/HGR-r202-prediction-full-path.csv', \
# #     ['phylum', 'class', 'order', 'family', 'genus'], '/mnt/sda/DeepMicrobes-data/labeled_genome-r202')
# # print("HGR single child are:", HGR_single_child)
# HGR_single_child = ['g__UMGS75', 'g__Proteus', 'c__Elusimicrobia', 'g__CAG-631', 'p__Fusobacteriota', 'c__Fusobacteriia', 'g__Amedibacterium', 'p__Firmicutes_C', 'o__ML615J-28', 'g__CAG-288', 'g__CAG-603', 'g__Amedibacillus', 'o__Treponematales', 'o__RF39', 'g__CAG-353', 'g__Pediococcus', 'p__Elusimicrobiota', 'g__QAMX01', 'f__Turicibacteraceae', 'g__CAG-345', 'g__Bacteroides_F', 'g__Eggerthella', 'f__CAG-631', 'g__Ruminococcus_F', 'f__Treponemataceae', 'g__Clostridium_A', 'f__Streptococcaceae', 'g__Clostridium_AP', 'f__Akkermansiaceae', 'f__UBA11471', 'g__Massilicoli', 'o__Elusimicrobiales', 'g__Turicimonas', 'c__Coriobacteriia', 'o__Haloplasmatales_A', 'o__Acholeplasmatales', 'g__CAG-988', 'g__Tidjanibacter', 'g__CAG-1031', 'f__QAMX01', 'o__Acidaminococcales', 'g__CAG-964', 'o__Verrucomicrobiales', 'g__F0040', 'p__Bacteroidota', 'p__Firmicutes', 'f__Bifidobacteriaceae', 'f__Barnesiellaceae']
# update_single_child(HGR_single_child, './outputs-HGR-r202-archive3', 'HGR-r202-archive3')


# print("GTDB")
# # GTDB_single_child = find_single_child('~/MT-MAG/outputs-GTDB-r202-archive3/GTDB-r202-prediction-full-path.csv', \
# #     ['domain', 'phylum', 'class', 'order', 'family', 'genus'], '/mnt/sda/MLDSP-samples-r202')
# # print("GTDB single child are:", GTDB_single_child)
# GTDB_single_child = ['g__Kandleria', 'g__RUG708', 'g__RUG714', 'g__UBA9722', 'c__Ozemobacteria', 'c__Desulfovibrionia', 'g__RUG678', 'c__Methanobacteria', 'f__RUG350', 'g__RUG147', 'g__UBA2942', 'o__RF39', 'g__RUG100', 'f__RUG033', 'f__UBA1188', 'f__UBA3663', 'c__Clostridia_A', 'p__Riflebacteria', 'p__RUG730', 'g__RUG013', 'g__CADAUA01', 'o__Ozemobacterales', 'g__RUG334']
# update_single_child(GTDB_single_child, './outputs-GTDB-r202-archive3', 'GTDB-r202-archive3')



