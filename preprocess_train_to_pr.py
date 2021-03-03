import sys
import pandas as pd 
import openpyxl
import os 

file = sys.argv[1]

pre_sheet_names = pd.ExcelFile(file).sheet_names
print("pre_sheet_names are:", pre_sheet_names)

df_merged = pd.read_excel(file, sheet_name = "quadratic-svm-score1", index_col=0, header=0)

for i in range(len(pre_sheet_names)):
    sheet = pre_sheet_names[i]
    df = pd.read_excel(file, sheet_name = sheet, index_col=0, header=0)
    df_merged = pd.concat([df_merged, df])

classes = df_merged.columns.tolist()
print("classes are:", classes)
for i in range(len(classes)-2):
    c = classes[i]
    index = classes.index(c)+1
    print("index is:", index)
    df_merged = df_merged.replace({'prediction': {index: c}, 'actual': {index: c}})
    print(df_merged)



for i in range(len(classes)-2):
    c = classes[i]
    print("saving", c)
    with pd.ExcelWriter(file, engine="openpyxl", mode='a') as writer: 
        df_subset = df_merged.loc[df_merged['actual'] == c]
        df_subset.to_excel(writer, sheet_name = c+"-b-p", index=True)
        writer.save()
        writer.close()



wb = openpyxl.load_workbook(file)
for sheet in pre_sheet_names:
    del wb[sheet]
wb.save(file)

os.system("python3 run_add_max.py "+file)



