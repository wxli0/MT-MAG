""" 
Add "rejection-f" column to the sheet (:param sheet_name) in a file \
    (:param file_name). The "rejection-f" represents the final decision baesd \
        on "max" and the rejection threshold (:param threshold_dict)
    
    Command line arguments:
    :param sys.argv[1]: file_path. The file path where MT-MAG classification \
        result is stored in 
    :type sys.argv[1]: str
    :param sys.argv[2]: sheet_name. The sheet of results that we are manipulating
    :type sys.argv[2]: str
    :param sys.argv[3]: rejection_dict. The rejection threshold dictionary with \
        keys being the child class names, and values being the rejection \
            thresholds for the child classes.
"""

import json
import openpyxl
import pandas as pd 
import os
import sys


file_path = sys.argv[1]
sheet = sys.argv[2]
threshold_dict = {}
if os.path.exists(sys.argv[3]):
    threshold_dict = json.load(open(sys.argv[3]))

df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)

rejection_f = []
for index, row in df.iterrows():
    # print("here is:", row['prediction'])
    # print("threshold_dict is", threshold_dict)
    alpha=0
    if row['prediction'] in threshold_dict:
        alpha = threshold_dict[row['prediction']]
    if row['max'] < alpha:
        rejection_f.append(row['prediction']+'(reject)')
    else: # if we are just classifying the genomes without rejection threshods 
        rejection_f.append(row['prediction'])
if 'rejection-f' in df.columns:
    del df['rejection-f']
df['rejection-f'] = rejection_f

wb = openpyxl.load_workbook(file_path)
del wb[sheet]

mode = 'w'
if len(wb.sheetnames) != 0:
    wb.save(file_path)
    mode = 'a'

with pd.ExcelWriter(file_path, engine="openpyxl", mode=mode) as writer:  
    df.to_excel(writer, sheet_name = sheet, index=True)
writer.save()
writer.close()



