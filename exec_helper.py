"""
Check missing predictions in the classification result files (GTDB and HGR)

No command line arguments are required
"""

import getpass
import os
import pandas as pd 
import subprocess

def check_missing(pred_path, ranks, root_taxon, base_path, test_dir):
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
    if not os.path.exists(pred_path):
        df = pd.DataFrame(columns=ranks)
        df['Row'] = os.listdir(os.path.join(base_path, test_dir))
        df = df.set_index('Row')
        df.to_csv(pred_path, header=True, index=True)
    df = pd.read_csv(pred_path, index_col=0, header=0, dtype = str)
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


def exec_phase(missing_ranks, data_type, base_path, test_dir, partial):
    """
    Iterate over missing ranks (missing_ranks) for task with data type (data_type) 
    
    :param missing_ranks: missing ranks to be classified. Outputs from check_missing
    :type missing_ranks: List[str]
    :param data_type: data type of the task. 'HGR-r202' or 'GTDB-r202'
    :type data_type: str
    :param base_path: training dataset path
    :type base_path: str
    :param test_dir: test dataset directory within the training dataset path
    :type test_dir: str
    :param partial: enable partial classification or not
    :type partial: bool
    """
    user_name = getpass.getuser()
    for rank in missing_ranks:
        classes = missing_ranks[rank]
        if len(classes) != 0:
            for c in classes:
                if not os.path.isdir(os.path.join(base_path, test_dir, c)): # group_pred has not grouped class c
                    continue 
                if c is None:
                    raise Exception("missing first taxon classification")
                running_proc = str(subprocess.check_output(\
                    "ps aux|grep "+user_name+"|grep "+"'"+ "phase.sh -s "+c+" -d "+data_type+"'", shell=True))
                proc_all =  str(subprocess.check_output("screen -ls", shell=True))
                if running_proc.count('\\n') <= 2 and proc_all.count('\\n') <= 40:
                    if not partial:
                        os.system(\
                            'screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d ' +  data_type + ' -b ' +base_path + ' -t '+ test_dir + '"')
                        print(\
                            'done screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d ' +  data_type + ' -b ' +base_path + ' -t '+ test_dir + '"')
                    else:
                        os.system(\
                            'screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d ' +  data_type + ' -b ' +base_path + ' -t '+ test_dir + ' -a ''"')
                        print(\
                            'done screen -dm bash -c "cd ~/MLDSP; bash phase.sh -s '+c + ' -d ' +  data_type + ' -b ' +base_path + ' -t '+ test_dir + ' -a ''"')
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
