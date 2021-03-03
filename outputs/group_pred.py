import sys
import pandas as pd 
import json
import os
from shutil import copyfile
import platform

# e.g. python3 group_pred.py order
taxon = sys.argv[1]

base_path = "/Users/wanxinli/Desktop/project/MLDSP-desktop/samples/" # run locally
if platform.platform()[:5] == 'Linux':
    base_path = "/home/w328li/MLDSP/samples/"

MLDSP_pred_path = "outputs/MLDSP-prediction-full-path.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
print(MLDSP_df)

for index, row in  MLDSP_df:
    label = row[taxon] != ''
    if row[taxon] != '':
        if not os.path.isdir(base_path+"rumen_mags/"+label):
            os.mkdir(base_path+"rumen_mags/"+label)
        copyfile(base_path+"rumen_mags/all/"+index, base_path+"rumen_mags/"+label+"/"+index)
        

