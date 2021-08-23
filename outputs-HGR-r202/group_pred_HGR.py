import sys
import pandas as pd 
import os
from shutil import copyfile

# e.g. python3 group_pred.py order
taxon = sys.argv[1]

base_path = "/mnt/sda/DeepMicrobes-data/"

MLDSP_pred_path = "./outputs-HGR-r202/HGR-prediction-full-path.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
print(MLDSP_df)

created = []
for index, row in  MLDSP_df.iterrows():
    label = row[taxon]
    index_str = str(index)
    if index_str.endswith('_1') or index_str.endswith('_2'):
        continue
    # print("label is:", label)
    if not str(label) == 'nan':
        if not os.path.isdir(base_path+"labeled_genome-r202/hgr_mags/"+label):
            created.append(label)
            os.mkdir(base_path+"labeled_genome-r202/hgr_mags/"+label)
            print("created", base_path+"labeled_genome-r202/hgr_mags/"+label)
        copyfile(base_path+"mag_reads_250bp_1w_200000/"+index_str+".fa", base_path+"labeled_genome-r202/hgr_mags/"+label+"/"+index_str+".fa")
        