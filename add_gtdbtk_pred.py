import sys
import pandas as pd 
import openpyxl

# e.g. python3 add_gtdbtk_pred.py c__Bacteroidia.xlsx c__Bacteroidia_pred-t-p order
file_path = sys.argv[1]
sheet = sys.argv[2]
taxon = sys.argv[3]

gtdbtk_df = pd.read_csv("/Users/wanxinli/Desktop/project/MLDSP-desktop/data/DS_10283_3009/GTDB-Tk_classification.csv", header=0, index_col=0)
df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)

gtdbtk_pred_list = []

for index, row in df.iterrows():
    if index.endswith('.fasta'):
        index = index[:-6]
    gtdbtk_pred = gtdbtk_df.loc[index][taxon]
    gtdbtk_pred_list.append(gtdbtk_pred)

df['gtdb-Tk'] = gtdbtk_pred_list

wb = openpyxl.load_workbook(file_path)
del wb[sheet]
wb.save(file_path)

with pd.ExcelWriter(file_path, engine="openpyxl", mode='a') as writer:  
    df.to_excel(writer, sheet_name = sheet, index=True)
writer.save()
writer.close()
