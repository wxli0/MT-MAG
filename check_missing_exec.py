"""
Check missing predictions in the classification result files (GTDB and HGR)

No command line arguments are required
"""

import getpass
import os
import pandas as pd 
import subprocess
import sys


def check_missing(path, ranks, root_taxon):
    """
    Checks ranks with incomplete predictions in the classification result path
    :param path: path of the classification result file
    :type path: str
    :param ranks: a list of ranks in the classification result file
    :type ranks: List[str]
    :param root_taxon: str
    :type root_taxon: the root taxon to start classification
    """
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)
    first_rank_res = list(df[ranks[0]])
    first_rank_str_res = [str(x) for x in first_rank_res]
    if first_rank_str_res == ['nan']:
        return {'root': root_taxon}

    # init missing_ranks
    missing_ranks = {}
    for r in ranks:
        missing_ranks[r] = []

    for index, row in df.iterrows():
        pre_pred = None
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


def exec_phase(missing_ranks, data_type, suffix=""):
    """
    Iterate over missing ranks (missing_ranks) for task with data type (data_type) 
    
    :param missing_ranks: missing ranks to be classified. Outputs from check_missing
    :type missing_ranks: List[str]
    :param data_type: data type of the task. 'HGR' or 'GTDB'
    :type data_type: str
    :param suffix: suffix of the folders in data_dir
    :type suffix: str
    """
    user_name = getpass.getuser()
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
                if c is None:
                    raise Exception("missing first taxon classification")
                running_proc = str(subprocess.check_output("ps aux|grep "+user_name+"|grep "+c, shell=True))
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


exec = False
if len(sys.argv) == 2:
    exec = sys.argv[1]

# execute the commands

path1 = os.path.join("./outputs-GTDB-r202/GTDB-prediction-full-path.csv")
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
root_taxon1 = 'root'
mrs1 = check_missing(path1, ranks1, root_taxon1)
data_dir1 = "/mnt/sda/MLDSP-samples-r202/"
suffix1 = ""

path2 = os.path.join("./outputs-HGR-r202/HGR-prediction-full-path.csv")
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
root_taxon2 = 'd__Bacteria'
mrs2 = check_missing(path2, ranks2, root_taxon2)
data_dir2 = "/mnt/sda/DeepMicrobes-data/labeled_genome-r202/"
suffix2 = "_split_pruned"
print("HGR missing ranks are:", mrs2)
if exec:
    exec_phase(mrs2, 'HGR', suffix=suffix1)

print("GTDB missing ranks are:", mrs1)
if exec:
    exec_phase(mrs1, 'GTDB', suffix=suffix2)
