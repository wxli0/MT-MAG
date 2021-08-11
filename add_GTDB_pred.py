from filelock import FileLock
import math
import openpyxl
import pandas as pd
import sys

""" 
Add MT-MAG classification of Task 1 (training dataset: GTDB) into \
    the classification result file

    Command line arguments:
    :param sys.argv[1]: file_path, file path where MT-MAG classification result \
        is stored in 
    :type file_path: str
"""

print("waiting to acqure add_GTDB_pred lock")
with FileLock("lock/add_GTDB_pred.lock"):
    print("Lock in add_GTDB_pred acquired.")
    file_path = sys.argv[1]
    file_short = file_path.split('/')[-1]
    ver = file_path.split('/')[0].split('-')[-1]
    sheet = file_short[:-5]+"_pred-t-p"
    if len(sys.argv) == 3:
        sheet = sys.argv[2]
    MLDSP_pred_path = "outputs-"+ver+"/MLDSP-prediction-full-path.csv"

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
    MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
    for index, row in df.iterrows():
        MLDSP_df.at[index[:-3], taxon] = row['rejection-f'] # 'prediction' for complete.csv

    MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)
    print("Lock in add_GTDB_pred acquired.")
