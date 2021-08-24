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
    first_rank_str_res = list(set([str(x) for x in first_rank_res]))
    if first_rank_str_res == ['nan']:
        return {'root': [root_taxon]}

    # init missing_ranks
    missing_ranks = {}
    for r in ranks:
        missing_ranks[r] = []

    for index, _ in df.iterrows():
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


def exec_phase(missing_ranks, data_type):
    """
    Iterate over missing ranks (missing_ranks) for task with data type (data_type) 
    
    :param missing_ranks: missing ranks to be classified. Outputs from check_missing
    :type missing_ranks: List[str]
    :param data_type: data type of the task. 'HGR' or 'GTDB'
    :type data_type: str
    """
    user_name = getpass.getuser()
    for rank in missing_ranks:
        classes = missing_ranks[rank]
        if len(classes) != 0:
            for c in classes:
                if c is None:
                    raise Exception("missing first taxon classification")
                running_proc = str(subprocess.check_output(\
                    "ps aux|grep "+user_name+"|grep "+"'"+ "phase.sh -s "+c+"'", shell=True))
                proc_all =  str(subprocess.check_output("screen -ls", shell=True))
                if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40:
                    os.system('screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d ' +  data_type + '"')
                    print('enter screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d '+ data_type + '"')

                elif proc_all.count('\\n') > 40:
                    print('too many processes running')
                else:
                    print(c, "in " + data_type + " running process")


exec = False
if len(sys.argv) == 2:
    exec = sys.argv[1]

# execute the commands

# path1 = os.path.join("./outputs-GTDB-r202/GTDB-prediction-full-path.csv")
# ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
# root_taxon1 = 'root'
# mrs1 = check_missing(path1, ranks1, root_taxon1)

# print("GTDB missing ranks are:", mrs1)
# if exec:
#     exec_phase(mrs1, 'GTDB')

path2 = os.path.join("./outputs-HGR-r202/HGR-prediction-full-path.csv")
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
root_taxon2 = 'd__Bacteria'
mrs2 = check_missing(path2, ranks2, root_taxon2)

print("HGR missing ranks are:", mrs2)
if exec:
    exec_phase(mrs2, 'HGR')


