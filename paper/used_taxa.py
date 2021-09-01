import json
import os
import sys


data_type = sys.argv[1]
rank = sys.argv[2]

json_data = json.load(open(os.path.join('task_metadata', data_type+".json")))
base_path = json_data['base_path']
ranks = json_data['ranks']

if rank != ranks[-1]:
    for file in os.listdir(base_path):
        



