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
base_path = "/Users/wanxinli/Desktop/project/MLDSP-desktop/samples/" # run locally
if platform.platform()[:5] == 'Linux':
    base_path = "/mnt/sda/MLDSP-samples-r202/"
    BK_path = "/home/w328li/BlindKameris-new/"

MLDSP_pred_path = BK_path+"outputs-r202/MLDSP-prediction-full-path.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
print(MLDSP_df)

for index, row in  MLDSP_df.iterrows():
    label = row[taxon]
    print("label is:", label)
    if not str(label) == 'nan':
        print("enter")
        if not os.path.isdir(base_path+"rumen_mags/"+label):
            os.mkdir(base_path+"rumen_mags/"+label)
        copyfile(base_path+"rumen_mags/root/"+index+"sta", base_path+"rumen_mags/"+label+"/"+index+"sta")
        
