import sys
import os
import pandas as pd 
import openpyxl

# alpha: changed manually
# argv[1]: file_name
# argv[2]: sheet_name
# argv[3]: alpha, threshold
# e.g.

file_path = sys.argv[1]
sheet = sys.argv[2]
alpha = float(sys.argv[3])

df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)
df['rejection-'+str(alpha)] = df.apply(lambda row: 'reject' if row['max'] < alpha else row['prediction'], axis=1)

wb = openpyxl.load_workbook(file_path)
del wb[sheet]
wb.save(file_path)

with pd.ExcelWriter(file_path, engine="openpyxl", mode='a') as writer:  
    df.to_excel(writer, sheet_name = sheet, index=True)
writer.save()
writer.close()



