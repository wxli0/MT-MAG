import sys
import pandas as pd 
import openpyxl
import os 

file = sys.argv[1]
rej_file = sys.argv[2]

df = pd.read_excel(file, sheet_name = "quadratic-svm-score", index_col=0, header=0)


classes = df.columns.tolist()
print("classes are:", classes)
for i in range(len(classes)-1):
    c = classes[i]
    index = classes.index(c)+1
    print("index is:", index)
    df = df.replace({'prediction': {index: "-".join(c.split('-')[1:])}})




with pd.ExcelWriter(file, engine="openpyxl", mode='a') as writer: 
    df.to_excel(writer, sheet_name = file.split('/')[-1][:-5]+"_pred-t-p", index=True)
    writer.save()
    writer.close()



wb = openpyxl.load_workbook(file)
del wb["quadratic-svm-score"]
wb.save(file)

os.system("python3 run_add_max.py "+file)

# os.system("python3 run_rejection_f.py "+file+" " + rej_file)


