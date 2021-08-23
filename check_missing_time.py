"""
Checks missing predictions in HGR/GTDB-prediction-full-path.csv.

No command line arguments are required.
"""

import getpass
import pandas as pd
import os
import subprocess


def check_missing(path, time_cat):
    """
    Determines the single child genus and query instances with GTDB-tk classified \
        species not exist in training dataset, and single-child genera
    :param data_dir: training dataset directory
    :type data_dir: str
    :param path: MT-MAG and GTDB-tk result path
    :type path: str
    """
    df = pd.read_csv(path, index_col=0, header=0, dtype=str)
    missing_ranks = []
    for index, row in df.iterrows():
        if str(row[time_cat]) == "nan":
            missing_ranks.append(index)

    return missing_ranks


path1 = os.path.join('./outputs-HGR-r202/time.csv')
time_cat1 = 'rej_time'
missing_ranks1 = check_missing(path1, time_cat1)

user_name = getpass.getuser()
for rank in missing_ranks1:
    running_proc = str(subprocess.check_output("ps aux|grep "+user_name+"|grep "+rank, shell=True))
    proc_all =  str(subprocess.check_output("screen -ls", shell=True))
    if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40:
        os.system('screen -dm bash -c "cd ~/MLDSP; bash phase_HGR_3_4.sh '+rank + '"')
        print('enter screen -dm bash -c "cd ~/MLDSP; bash phase_HGR_3_4.sh '+rank + '"')
    elif proc_all.count('\\n') > 40:
        print('too many processes running')
    else:
        print(rank, "in GTDB running process")
