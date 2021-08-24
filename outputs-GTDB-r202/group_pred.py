import config
import os
import pandas as pd 
from shutil import copyfile
import sys

# e.g. python3 group_pred.py order
taxon = sys.argv[1]


MLDSP_pred_path = "./outputs-GTDB-r202/GTDB-prediction-full-path.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
print(MLDSP_df)

for index, row in  MLDSP_df.iterrows():
    label = row[taxon]
    # print("label is:", label)
    if not str(label) == 'nan':
        if not os.path.isdir(os.path.join(config.GTDB_train_path, "rumen_mags/"+label)):
            os.mkdir(os.path.join(config.GTDB_train_path, "rumen_mags/"+label))
            print("created", os.path.join(config.GTDB_train_path, "rumen_mags/"+label))
        copyfile(os.path.join(config.GTDB_train_path, "rumen_mags/root/"+index+"sta"), \
            os.path.join(config.GTDB_train_path, "rumen_mags/"+label+"/"+index+"sta"))
        

