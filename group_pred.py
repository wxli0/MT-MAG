import os
import pandas as pd 
from shutil import copyfile


# e.g. python3 group_pred.py order

def group_pred(pred_path, test_dir, rank):
    pred_df =  pd.read_csv(pred_path, index_col=0, header=0, dtype = str)
    print(pred_df)

    for index, row in  pred_df.iterrows():
        label = row[rank]
        if not str(label) == 'nan':
            if not os.path.isdir(os.path.join(test_dir, label)):
                os.mkdir(os.path.join(test_dir, label))
                print("created", os.path.join(test_dir, label))
            copyfile(os.path.join(test_dir, index), \
                os.path.join(test_dir, index))

def group_pred_all_ranks(pred_path, test_dir, ranks):
    for rank in ranks:
        group_pred(pred_path, test_dir, rank)
            

