import sys
import pandas as pd
import math
import openpyxl

from filelock import FileLock

print("waiting to acqure add_HGR_pred lock")
with FileLock("add_HGR_pred.lock"):
    print("Lock in add_HGR_pred acquired.")

    file_path = sys.argv[1]
    file_short = file_path.split('/')[-1]
    ver = file_path.split('/')[0].split('-')[-1]
    sheet = file_short[:-5]+"_pred-t-p"
    if len(sys.argv) == 3:
        sheet = sys.argv[2]
    pred_path = "outputs-HGR-"+ver+"/HGR-prediction-full-path.csv"

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
        if (not index.endswith("_1")) and (not index.endswith("_2")):
            cur_pred = pred_df.at[index[:-3], taxon]
            if cur_pred in row['rejection-f']:
                pred_df.at[index[:-3], taxon] = row['rejection-f'] # 'prediction' for complete.csv
            elif str(cur_pred) != 'nan':
                print("Invalid:", index, "previous pred:", cur_pred, "new pred:", row['rejection-f'])
            
    pred_df.to_csv(pred_path, index=True, header=True)
    print("Lock in add_HGR_pred released.")
