import sys
import pandas as pd 
import json
import os
from shutil import copyfile
import platform
import shutil
import numpy as np

# e.g. python3 group_pred.py order
taxon = sys.argv[1]

BK_path = "/Users/wanxinli/Desktop/project/BlindKameris-new/"
base_path = "/mnt/sda/DeepMicrobes-data/" 
if platform.platform()[:5] == 'Linux':
    BK_path = "/home/w328li/BlindKameris-new/"

MLDSP_pred_path = BK_path+"outputs_HGR/HGR-prediction-full-path.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
print(MLDSP_df)

for index, row in  MLDSP_df.iterrows():
    label = row[taxon]
    print("label is:", label)
    if not str(label) == 'nan':
        print("enter")
        if not os.path.isdir(base_path+"hgr_mags/"+label):
            os.mkdir(base_path+"hgr_mags/"+label)
        copyfile(base_path+"mag_reads_250bp_1w_20000/"+index, base_path+"hgr_mags/"+label+"/"+index)
        

