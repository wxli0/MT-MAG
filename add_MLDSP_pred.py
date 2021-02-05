import sys
import pandas as pd

file = sys.argv[1]
file_short = file.split('/')[-1]
sheet = file_short[:-5]+"_pred_t"

taxon = ""
if sheet.startswith('d'):
    taxon = "phylum"
elif sheet.startswith('p'):
    taxon = "class"
elif sheet.startswith('c'):
    taxon = "order"
elif sheet.startswith('o'):
    taxon = "family"

df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)
MLDSP_df =  pd.read_excel("outputs/MLDSP-prediction", index_col=0, header=0, sheet_name="Sheet1")