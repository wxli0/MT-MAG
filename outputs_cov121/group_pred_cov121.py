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
base_path = "/mnt/sda/MLDSP-samples/" 
if platform.platform()[:5] == 'Linux':
    BK_path = "/home/w328li/BlindKameris-new/"

cov121_pred_path = BK_path+"outputs_cov121/cov121-prediction-full-path.csv"
cov121_df =  pd.read_csv(cov121_pred_path, index_col=0, header=0, dtype = str)
print(cov121_df)

for index, row in  cov121_df.iterrows():
    label = row[taxon]
    print("label is:", label)
    if not str(label) == 'nan':
        print("enter")
        if not os.path.isdir(base_path+"unknown_species_cov1x_combined/"+label):
            os.mkdir(base_path+"unknown_species_cov1x_combined/"+label)
        copyfile(base_path+"unknown_species_cov1x_combined/"+index, base_path+"unknown_species_cov1x_combined/"+label+"/"+index)
        

