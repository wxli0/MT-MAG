import sys
import pandas as pd
import math
import openpyxl

from filelock import FileLock

with FileLock("myfile.txt.lock"):
    print("Lock in add_HGR_pred acquired.")

    file_path = sys.argv[1]
    file_short = file_path.split('/')[-1]
    ver = file_path.split('/')[0].split('-')[-1]
    sheet = file_short[:-5]+"_pred-t-p"
    if len(sys.argv) == 3:
        sheet = sys.argv[2]
    MLDSP_pred_path = "outputs-HGR-"+ver+"/HGR-prediction-full-path.csv"

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

    df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)
    MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
    for index, row in df.iterrows():
        MLDSP_df.at[index[:-3], taxon] = row['prediction'] # used to be 'rejection-f'

    MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)
    print("Lock in add_HGR_pred released.")
