import sys
import pandas as pd
import math
import openpyxl

# e.g. 
file_path = sys.argv[1]
file_short = file_path.split('/')[-1]
sheet = file_short[:-5]+"_pred-t-p"
if len(sys.argv) == 3:
    sheet = sys.argv[2]
MLDSP_pred_path = "outputs_HGR/HGR-prediction-full-path.csv"

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
# print(MLDSP_df)
# print(math.isnan(MLDSP_df.loc['RUG518']['family']))
for index, row in df.iterrows():
    print("index is:", index)
    print("taxon is:", taxon)
    print("rejection-f is:", row['rejection-f'])
    # if not math.isnan(MLDSP_df.loc[index[:-3]][taxon]):
    #     print("success")
    #     raise Exception()
    MLDSP_df.at[index[:-3], taxon] = row['rejection-f']

print(MLDSP_df)
print(MLDSP_df.shape)
print(df.shape)

MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)