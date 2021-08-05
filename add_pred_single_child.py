import sys
import pandas as pd
import math
import openpyxl
import time

from filelock import FileLock

print("waiting to acqure add_pred lock")
with FileLock("add_pred.lock"):
    print("Lock in add_pred acquired.")

    file_path = sys.argv[2]
    type = sys.argv[1]
    file_short = file_path.split('/')[-1]
    ver = file_path.split('/')[0].split('-')[-1]
    sheet = file_short[:-5]+"_pred-t-p"
    pred_name = ""
    if type == 'HGR':
        pred_dir = "outputs-HGR-"+ver
        pred_name = "HGR-prediction-full-path.csv"
    elif type == 'GTDB':
        pred_dir = "outputs-"+ver
        pred_name = "MLDSP-prediction-full-path.csv"

    
    pred_path = pred_dir+"/"+pred_name

    taxon = ""
    if sheet.startswith('d') or sheet.startswith('e'):
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

    taxon_df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)
    pred_df =  pd.read_csv(pred_path, index_col=0, header=0, dtype = str)
    for index, row in taxon_df.iterrows():
        short_index = index
        if type == 'HGR':
            short_index = index[:-3]
        cur_pred = pred_df.at[short_index, taxon]
        if cur_pred in row['rejection-f']:
            pred_df.at[short_index[:-3], taxon] = row['rejection-f'] # 'prediction' for complete.csv
        elif str(cur_pred) != 'nan':
            with FileLock("conflict.lock"):
                with open('myfile.dat', 'w+') as file:
                    file.write("file_path is:", file_path, "invalid:", index, \
                        "previous pred:", cur_pred, "new pred:", row['rejection-f'])
            
    pred_df.to_csv(pred_path, index=True, header=True)
    print("Lock in add_pred released.")
