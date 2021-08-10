
from filelock import FileLock
import math
import openpyxl
import pandas as pd
import sys
import time


""" 
Add MT-MAG classification result store in a file (:param file_path) of a specific task \
    type (:param type) into the classification result file. The classification \
        task is a single-child taxon classification.

    Command line arguments:
    :param sys.argv[1]: file_path, file path where MT-MAG classification result \
        is stored in 
    :type file_path: str
    :param sys.argv[2]: type of the task, with "GTDB" represents Task 1 and \
        "HGR" represents Task 2
    :type type: str
"""

print("waiting to acqure add_pred lock")
with FileLock("lock/add_pred.lock"):
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
        elif type == 'GTDB':
            short_index = index[:-3]
        prev_pred = pred_df.at[short_index, taxon]
        if str(prev_pred) in row['rejection-f'] or str(prev_pred) == 'nan':
            pred_df.at[short_index, taxon] = row['rejection-f'] # 'prediction' for complete.csv
        elif str(prev_pred) != 'nan':
            with FileLock("conflict.lock"):
                with open('conflict.txt', 'a') as file:
                    file.write("file_path is: "+file_path+" short_index is: "+short_index+ \
                        " previous pred: "+prev_pred+" new pred: "+row['rejection-f']+"\n")
            
    pred_df.to_csv(pred_path, index=True, header=True)
    print("Lock in add_pred released.")
