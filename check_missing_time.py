import pandas as pd
import os
import sys
import platform
import subprocess

# check missing predictions in HGR/MLDSP-prediction-full-path.csv


def check_missing(path, time_cat):
    df = pd.read_csv(path, index_col=0, header=0, dtype=str)

    missing_ranks = []
    for index, row in df.iterrows():
        if str(row[time_cat]) == "nan":
            missing_ranks.append(index)

    return missing_ranks

base_path = "/Users/wanxinli/Desktop/project.nosync/"
if platform.platform()[:5] == 'Linux':
    base_path = "/home/w328li/"

path1 = base_path+'BlindKameris-new/outputs-r202/time.csv'
time_cat1 = 'rej_time'
missing_ranks1 = check_missing(path1, time_cat1)

for rank in missing_ranks1:
    running_proc = str(subprocess.check_output("ps aux|grep w328li|grep "+rank, shell=True))
    proc_all =  str(subprocess.check_output("screen -ls", shell=True))
    if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40:
        os.system('screen -dm bash -c "cd ~/MLDSP; bash phase_3_4.sh '+rank + '"')
        print('enter screen -dm bash -c "cd ~/MLDSP; bash phase_3_4.sh '+rank + '"')
    elif proc_all.count('\\n') > 40:
        print('too many processes running')
    else:
        print(rank, "in GTDB running process")
