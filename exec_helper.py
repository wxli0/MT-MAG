"""
Check missing predictions in the classification result files (GTDB and HGR)

No command line arguments are required
"""

import getpass
import os
import pandas as pd 
import subprocess

def check_missing(path, ranks, root_taxon, test_dir):
    """
    Checks ranks with incomplete predictions in the classification result path
    :param path: path of the classification result file
    :type path: str
    :param ranks: a list of ranks in the classification result file
    :type ranks: List[str]
    :param root_taxon: str
    :type root_taxon: the root taxon to start classification
    """

    # create a clean result file if does not exist
    if not os.path.exists(path):
        if test_dir is None: 
            raise Exception("missing --test_data for check_missing_exec.py")
        df = pd.DataFrame(columns=ranks)
        df['Row'] = os.listdir(test_dir)
        df = df.set_index('Row')
        df.to_csv(path, header=True, index=True)
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
                if pre_pred not in missing_ranks[r]:
                    missing_ranks[r].append(pre_pred)
                break
            pre_pred = cur_pred

    return missing_ranks


def exec_phase(missing_ranks, data_type, base_path = None, test_dir = None):
    """
    Iterate over missing ranks (missing_ranks) for task with data type (data_type) 
    
    :param missing_ranks: missing ranks to be classified. Outputs from check_missing
    :type missing_ranks: List[str]
    :param data_type: data type of the task. 'HGR-r202' or 'GTDB-r202'
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
                    "ps aux|grep "+user_name+"|grep "+"'"+ "phase.sh -s "+c+" -d "+data_type+"'", shell=True))
                proc_all =  str(subprocess.check_output("screen -ls", shell=True))
                if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40:
                    if data_type == 'GTDB-r202' or data_type == 'HGR-r202':
                        os.system(\
                            'screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d ' +  data_type + '"')
                        print(\
                            'enter screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d '+ data_type + '"')
                    else:
                        if base_path is None or test_dir is None:
                            raise Exception("base_path and test_dir are required arguments for data_type "+ data_type)
                        os.system(\
                            'screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d ' +  data_type + ' -b ' +base_path + ' -t '+ test_dir + '"')


                elif proc_all.count('\\n') > 40:
                    print('too many processes running')
                else:
                    print(c, "in " + data_type + " running process")

def push_changes():
    os.system('cd ~/MLDSP')
    os.system('git add .')
    os.system('git commit -m "updated outputs"')
    os.system('git push')
    os.system('cd ~/MT-MAG')
    os.system('git add .')
    os.system('git commit -m "updated outputs"')
    os.system('git push')
