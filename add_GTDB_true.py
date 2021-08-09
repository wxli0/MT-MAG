import sys
import pandas as pd
import math
import openpyxl

""" 
Add GTDB-Tk classification of Task 1 (training dataset: GTDB) into \
    the classification result file

    Fixed arguments:
    :param MLDSP_pred_path: file_path, file path of the classification file
    :type argv[1]: str
"""
# add GTDB-Tk classification of Task 1 (training dataset: GTDB) into classification result file
MLDSP_pred_path = "outputs/MLDSP-prediction.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
print(MLDSP_df)

GTDB_Tk_path = "/Users/wanxinli/Desktop/project/MLDSP-desktop/data/DS_10283_3009/GTDB-Tk_classification.csv"
GTDB_Tk_df = pd.read_csv(GTDB_Tk_path, index_col=0, header=0, dtype = str)
print(GTDB_Tk_df)

for index, row in MLDSP_df.iterrows(): 
    MLDSP_df.at[index, "GTDB-Tk-domain"] = GTDB_Tk_df.loc[index]["domain"]
    MLDSP_df.at[index, "GTDB-Tk-phylum"] = GTDB_Tk_df.loc[index]["phylum"]
    MLDSP_df.at[index, "GTDB-Tk-class"] = GTDB_Tk_df.loc[index]["class"]
    MLDSP_df.at[index, "GTDB-Tk-order"] = GTDB_Tk_df.loc[index]["order"]
    MLDSP_df.at[index, "GTDB-Tk-family"] = GTDB_Tk_df.loc[index]["family"]

print(MLDSP_df)
MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)