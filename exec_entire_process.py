"""
Script for grouping test sequences, and calling check_missing_pred 
periodically
"""

import json
import sys
sys.path.insert(0, '.')
import os
from subprocess import Popen, PIPE
import time

from group_pred import group_pred_all_ranks
from exec_helper import push_changes, check_missing, exec_phase, check_folders

metadata_path = sys.argv[1]

metadata = json.load(open(metadata_path))
ranks = metadata['ranks']
root_taxon = metadata['root_taxon']
data_type = metadata['data_type']
test_dir = metadata['test_dir']
base_path = metadata['base_path']
pred_path = './outputs-'+data_type+"/"+data_type+"-prediction-full-path.csv"
partial = False
if 'partial' in metadata:
    partial = metadata['partial']
accepted_CA = 0.9
if 'accepted_CA' in metadata:
    accepted_CA = metadata["accepted_CA"]
variability = 0.2
if 'variability' in metadata:
    variability = metadata["variability"]


check_folders(data_type, base_path, test_dir, pred_path, ranks, root_taxon)

i=0  
pre_proc_num=0
while True:
    print("===== iteration:", i, "=====")
    stdout = Popen('echo $(screen -ls)|grep -Po "[[:digit:]]+ *(?=Socket)"', shell=True, stdout=PIPE).stdout
    cur_proc_num = int(stdout.read())
    print("cur_proc_num is:", cur_proc_num)
    print("pre_proc_num is:", pre_proc_num)
    if (cur_proc_num != pre_proc_num) or (i == 0):
        # print("==== git commit ====")
        # push_changes()
        print("==== begin group_pred ====")
        group_pred_all_ranks(pred_path, base_path, test_dir, root_taxon, ranks[:-1])
        print("==== begin check_missing ====")
        missing_ranks = check_missing(pred_path, ranks, root_taxon, base_path, test_dir)
        print("missing_ranks are:", missing_ranks)
        if missing_ranks is None:
            print("==== DONE ====")
            break
        print('==== begin exec_phase ====')
        exec_phase(missing_ranks, data_type, base_path, test_dir, partial, accepted_CA, variability)
    else:
        print("No processes finished.")

    stdout = Popen('echo $(screen -ls)|grep -Po "[[:digit:]]+ *(?=Socket)"', shell=True, stdout=PIPE).stdout
    pre_proc_num=int(stdout.read())
    print("==== begin sleep 5 minutes at "+time.ctime()+" ====")
    time.sleep(300)
    i=i+1
