import sys
import pandas as pd
import math
import openpyxl

""" 
Add GTDB-Tk classification of Task 2 (training dataset: HGR) into \
    the classification result file

    Fixed arguments:
    :param MLDSP_pred_path: file_path, file path of the classification file
    :type argv[1]: str
"""

MLDSP_pred_path = "outputs_HGR/HGR-prediction-full-path.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
# print(MLDSP_df)

true_path = "/Users/wanxinli/Desktop/project/BlindKameris-new/outputs_HGR/Table_S2.csv"
true_df = pd.read_csv(true_path, index_col=0, header=1, dtype = str)
print(true_df)

for index, row in MLDSP_df.iterrows(): 
    print(index)
    MLDSP_df.at[index, "Phylum (reference)"] = true_df.loc[index[5:]]["Phylum (reference)"]
    MLDSP_df.at[index, "Class (reference)"] = true_df.loc[index[5:]]["Class (reference)"]
    MLDSP_df.at[index, "Order (reference)"] = true_df.loc[index[5:]]["Order (reference)"]
    MLDSP_df.at[index, "Family (reference)"] = true_df.loc[index[5:]]["Family (reference)"]
    MLDSP_df.at[index, "Genus (reference)"] = true_df.loc[index[5:]]["Genus (reference)"]

print(MLDSP_df)
MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)