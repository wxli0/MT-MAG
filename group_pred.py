import os
import pandas as pd 
from shutil import copyfile


# e.g. python3 group_pred.py order

def group_pred(pred_path, base_path, test_dir, all_test_dir, rank):
    pred_df =  pd.read_csv(pred_path, index_col=0, header=0, dtype = str)
    print(pred_df)

    for index, row in  pred_df.iterrows():
        label = row[rank]
        if not str(label) == 'nan':
            if not os.path.isdir(os.path.join(base_path, test_dir, label)):
                os.mkdir(os.path.join(base_path, test_dir, label))
                print("created", os.path.join(base_path, test_dir, label))
            copyfile(os.path.join(all_test_dir, index), \
                os.path.join(base_path, test_dir, label, index))

def group_pred_all_ranks(pred_path, base_path, test_dir, all_test_dir, ranks):
    for rank in ranks:
        group_pred(pred_path, base_path, test_dir, all_test_dir, rank)
            

