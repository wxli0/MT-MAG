import sys
import pandas as pd
import math
import openpyxl

file_path = sys.argv[1]
file_short = file_path.split('/')[-1]
sheet = file_short[:-5]+"_pred-t-p"
MLDSP_pred_path = "outputs/MLDSP-prediction.csv"

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
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
# print(MLDSP_df)
# print(math.isnan(MLDSP_df.loc['RUG518']['family']))
for index, row in df.iterrows():
    if not math.isnan(MLDSP_df.loc[index][taxon]):
        print("index is:", index)
        print("taxon is:", taxon)
        raise Exception()
    MLDSP_df.at[index, taxon] = row['rejection-f']

print(MLDSP_df)

MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)