import sys
import pandas as pd 
import json
import os
from shutil import copyfile
import platform

input_dict = json.load(open(sys.argv[1]))
file_path = input_dict['file_path']
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
    id = file[:-6]
    prediction = df[id]['rejection-f']
    dest = os.path.join(input_folder, prediction)
    if not os.path.isdir(dest):
        os.mkdir(dest)
    copyfile(file, dest)

