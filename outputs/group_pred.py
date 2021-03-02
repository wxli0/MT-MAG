import sys
import pandas as pd 
import json
import os
from shutil import copyfile
import platform

# e.g. python3 group_pred.py c__Bacilli.json
input_dict = json.load(open(sys.argv[1]))
file_path = input_dict['file_path']
sheet = file_path[:-5].split('/')[-1]+'_pred-t-p'
if 'sheet' in input_dict:
    sheet = input_dict['sheet']

base_path = "/Users/wanxinli/Desktop/project/MLDSP-desktop/samples/" # run locally
if platform.platform()[:5] == 'Linux':
    base_path = "/home/w328li/MLDSP/samples/"

input_folder = base_path+input_dict['input_folder']
output_folder = base_path+input_dict['output_folder']

pred_id_dict = {}

df = pd.read_excel(file_path, index_col=0, header=0, sheet_name=sheet)

for index, row in df.iterrows():
    prediction = row['rejection-f']
    if prediction in pred_id_dict:
        pred_id_dict[prediction].append(index)
    else:
        pred_id_dict[prediction] = [index]
    
print(pred_id_dict)

for file in os.listdir(input_folder):
    if file.endswith('.fasta'):
        id = file
        prediction = df.loc[id]['rejection-f']
        dest_folder = os.path.join(output_folder, prediction)
        src = os.path.join(input_folder, file)
        if not os.path.isdir(dest_folder):
            os.mkdir(dest_folder)
        copyfile(src, os.path.join(dest_folder, file))

