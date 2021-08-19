"""
Check missing predictions in the classification result files (GTDB and HGR)

No command line arguments are required
"""

import os
import pandas as pd 
import platform
import subprocess
import sys


def check_missing(path, ranks):
    """
    Checks ranks with incomplete predictions in the classification result path
    :param path: path of the classification result file
    :type path: str
    :param ranks: a list of ranks in the classification result file
    :type ranks: List[str]
    """
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)

    # init missing_ranks
    missing_ranks = {}
    for r in ranks:
        missing_ranks[r] = []

    for index, row in df.iterrows():
        pre_pred = 'root'
        for r in ranks:
            cur_pred = str(df.loc[index][r])
            if 'reject' in cur_pred:
                break
            if cur_pred == 'nan':
                # print(index, row)
                if pre_pred not in missing_ranks[r]:
                    missing_ranks[r].append(pre_pred)
                break
            pre_pred = cur_pred

    return missing_ranks


def exec_phase(missing_ranks, data_type):
    """
    Iterate over missing ranks (missing_ranks) for task with data type (data_type) 
    
    :param missing_ranks: missing ranks to be classified. Outputs from check_missing
    :type missing_ranks: List[str]
    :param data_type: data type of the task. 'HGR' or 'GTDB'
    :type data_type: str
    :param suffix: suffix of the folders in data_dir
    :type suffix: str
    """
    data_dir = ""
    suffix = ""
    if data_type == 'GTDB':
        data_dir = "/mnt/sda/MLDSP-samples-r202/"
    elif data_type == 'HGR':
        data_dir = "/mnt/sda/DeepMicrobes-data/labeled_genome-r202/"
        suffix = "_split_pruned"
    for rank in missing_ranks:
        classes = missing_ranks[rank]
        if len(classes) != 0:
            for c in classes:
                if c == 'root':
                    continue
                running_proc = str(subprocess.check_output("ps aux|grep w328li|grep "+c, shell=True))
                proc_all =  str(subprocess.check_output("screen -ls", shell=True))
                if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40:
                    if data_type == 'HGR' and not os.path.exists(data_dir+c+suffix):
                        os.system("python3 ~/DeepMicrobes/scripts/split_fasta_5000.py "+data_dir+c)
                        print("created", data_dir+c+suffix)
                    if len(os.listdir(data_dir+c+suffix)) > 1: # not single child taxon
                        os.system('screen -dm bash -c "cd ~/MLDSP; bash phase.sh '+c + ' ' + data_type + '"')
                        print('enter screen -dm bash -c "cd ~/MLDSP; bash phase.sh '+c + ' '+ data_type + '"')
                    else:
                        os.system(\
                            "screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_single.sh "+\
                                c+" "+data_type+"\"")
                        print("enter screen -dm bash -c "+"\"cd ~/MLDSP; bash phase_single.sh "+\
                                c+" "+data_type+"\"")
                elif proc_all.count('\\n') > 40:
                    print('too many processes running')
                else:
                    print(c, "in " + data_type + " running process")


base_path = "/Users/wanxinli/Desktop/project.nosync/"
if platform.platform()[:5] == 'Linux':
    base_path = "/home/w328li/"

exec = False
if len(sys.argv) == 2:
    exec = sys.argv[1]

# execute the commands

path1 = base_path+"BlindKameris-new/outputs-r202/MLDSP-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
mrs1 = check_missing(path1, ranks1)
data_dir1 = "/mnt/sda/MLDSP-samples-r202/"
suffix1 = ""

path2 = base_path+"BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
mrs2 = check_missing(path2, ranks2)
data_dir2 = "/mnt/sda/DeepMicrobes-data/labeled_genome-r202/"
suffix2 = "_split_pruned"
print("HGR missing ranks are:", mrs2)
if exec:
    exec_phase(mrs2, 'HGR')

print("GTDB missing ranks are:", mrs1)
if exec:
    exec_phase(mrs1, 'GTDB')
