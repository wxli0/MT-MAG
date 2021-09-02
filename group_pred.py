import os
import pandas as pd 
from shutil import copyfile


# e.g. python3 group_pred.py order
def group_pred(pred_path, base_path, test_dir, root_taxon, rank):
    """
    Groups test genomes in the test directory (test_dir) by predictions in \
        pred_path and rank. test_dir is stored inside base_path. The root taxon \
            for the task is root_taxon.
    
    :param pred_path: classification result file path. 
    :type pred_path: str
    :param base_path: base path of training and testing datasets
    :type base_path: str
    :param test_dir: name of the test directories inside base_path
    :type test_dir: str
    :param root_taxon: the root taxon of the task. i.e. the taxon that all all test \
        genomes belong to
    :type root_taxon: str
    :param rank: the rank in pred_path that we want to group test genomes by
    :type rank: str
    """
    pred_df =  pd.read_csv(pred_path, index_col=0, header=0, dtype = str)
    print(pred_df)

    all_test_dir = os.path.join(base_path, test_dir, root_taxon)
    for index, row in  pred_df.iterrows():
        label = row[rank]
        if not str(label) == 'nan':
            if not os.path.isdir(os.path.join(base_path, test_dir, label)):
                os.mkdir(os.path.join(base_path, test_dir, label))
                print("created", os.path.join(base_path, test_dir, label))
            copyfile(os.path.join(all_test_dir, index), \
                os.path.join(base_path, test_dir, label, index))


def group_pred_all_ranks(pred_path, base_path, test_dir, all_test_dir, ranks):
    """
    Groups test genomes in the test directory (test_dir) by predictions in \
        pred_path for all ranks. test_dir is stored inside base_path. The root taxon \
            for the task is root_taxon. Wrapper function for group_pred
    
    :param ranks: a list of available ranks in pred_path
    :type ranks: List[str]
    """
    for rank in ranks:
        group_pred(pred_path, base_path, test_dir, all_test_dir, rank)
            

