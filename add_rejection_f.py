import sys
import os
import pandas as pd 
import openpyxl
import json

# alpha: changed manually
# argv[1]: file_name
# argv[2]: sheet_name
# argv[3]: alpha, threshold
# e.g.

file_path = sys.argv[1]
sheet = sys.argv[2]
threshold_dict = json.load(open(sys.argv[3]))

df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)

rejection_f = []
for index, row in df.iterrows():
    alpha = threshold_dict[row['prediction']]
    if row['max'] < alpha:
        rejection_f.append(row['prediction']+'(reject)')
    else:
        rejection_f.append(row['prediction'])
if 'rejection-f' in df.columns:
    del df['rejection-f']
df['rejection-f'] = rejection_f

wb = openpyxl.load_workbook(file_path)
del wb[sheet]
wb.save(file_path)

with pd.ExcelWriter(file_path, engine="openpyxl", mode='a') as writer:  
    df.to_excel(writer, sheet_name = sheet, index=True)
writer.save()
writer.close()



