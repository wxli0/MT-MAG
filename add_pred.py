""" 
Add MT-MAG classification of Task 1 (training dataset: GTDB) into \
    the classification result file

    Command line arguments:
    :param sys.argv[1]: file_path, file path where MT-MAG classification result \
        is stored in 
    :type file_path: str
"""

from filelock import FileLock
import pandas as pd
import sys

file_path = sys.argv[1]
data_type = sys.argv[2]
file_short = file_path.split('/')[-1]
ver = file_path.split('/')[0].split('-')[-1]
sheet = file_short[:-5]+"_pred-t-p"
pred_path = "outputs-"+data_type+"-"+ver+"/"+data_type+"-prediction-full-path.csv"
lock_path="lock/add_"+data_type+"_pred.lock"

print("waiting to acqure add_GTDB_pred lock")
with FileLock(lock_path):
    print("Lock in add_pred acquired.")

    taxon = ""
    if sheet.startswith('r'):
        taxon = 'domain'
    elif sheet.startswith('d'):
        taxon = "phylum"
    elif sheet.startswith('p'):
        taxon = "class"
    elif sheet.startswith('c'):
        taxon = "order"
    elif sheet.startswith('o'):
        taxon = "family"
    elif sheet.startswith('f'):
        taxon = "genus"
    elif sheet.startswith('g'):
        taxon = "species"

    df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)
    pred_df =  pd.read_csv(pred_path, index_col=0, header=0, dtype = str)
    for index, row in df.iterrows():
        if data_type == "HGR" and (index.endswith("_1") or index.endswith("_2")):
            continue
        pred_df.at[index[:-3], taxon] = row['rejection-f'] # 'prediction' for complete.csv

    pred_df.to_csv(pred_path, index=True, header=True)
    print("Lock in add_pred acquired.")

