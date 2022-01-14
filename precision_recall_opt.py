"""
Calculates rejection thresholds based on a training result file, and a \
    testing result file for a taxon for a specific training dataset. This is \
        used for non-single-child taxons.

:param sys.argv[1]: file_name. Path of the training result file.
:type sys.argv[1]: str
:param sys.argv[2]: test_file.
:type sys.argv[2]: str
:param sys.argv[3]: data_type. Training data type of the classification Task. \
    GTDB or HGR.
:type sys.argb[3]: str

:Example precision_recall_opt.py outputs-GTDB-r202/d__Bacteria_train.xlsx outputs-GTDB-r202/d__Bacteria.xlsx GTDB
"""

import json 
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from multiprocess import Pool
import numpy as np 
import os
import pandas as pd
import platform
import statistics
import sys

# construct w_dfs
def df_taxon(taxon):
    print("construct df for:", taxon)
    b_sheet = taxon + '-b-p'
    b_df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
    for index, row in b_df.iterrows():
        pred = row['prediction']
        if pred != taxon: # add to w_df
            w_dfs[taxons.index(pred)].loc[index] = row

if __name__ ==  '__main__':
    gap = 0.01
    alphas = np.arange(0, 1+gap, gap).tolist()
    file_name = sys.argv[1]
    test_file = sys.argv[2]
    data_type = sys.argv[3]
    accepted_CA = float(sys.argv[4])
    variability = float(sys.argv[5])

    xls = pd.ExcelFile(file_name)
    precision = []
    recall = []
    weighted = []

    alpha_num = int(1/gap+1)

    taxons = [x[:-4] for x in xls.sheet_names]
    parent = file_name.split('/')[-1][:-11]

    # init w_dfs
    w_dfs = []
    for taxon in taxons:
        b_sheet = taxon + '-b-p'
        b_df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
        tmp_col = ['Row']
        tmp_col.extend(b_df.columns)
        w_df = pd.DataFrame(columns=tmp_col)
        w_df = w_df.set_index('Row')
        w_dfs.append(w_df)



    print("constructing dfs")
    p = Pool(10)
    all_thres = p.map(df_taxon, taxons)

    # read in test file
    test_df = pd.read_excel(test_file, sheet_name = 'quadratic-svm-score', header=0, index_col=0)
    existing_preds = list(set(test_df['prediction']))
    for i in range(len(existing_preds)):
        existing_preds[i] = int(existing_preds[i])-1


    BK_path = "./rejection-threshold-"+data_type+"/"
    if platform.platform()[:5] == 'Linux':
        BK_path = "./rejection-threshold-"+data_type+"/"
    if platform.node() == 'q.vector.local' or platform.node().startswith('guppy'):
        BK_path = "./rejection-threshold-"+data_type+"/"

    rej_path = BK_path+parent+'.json'

    print("constructing rej_dict")

    def taxon_recall(taxon):
        if os.path.exists(rej_path):
            rej_dict = json.load(open(rej_path))
            if taxon in rej_dict and rej_dict[taxon] is not None:
                print(taxon, "already in rej_dict")
                return  rej_dict[taxon]   
        taxon_index = taxons.index(taxon)
        if taxon_index not in existing_preds:
            print(taxon, "not in existing_preds")
            return None 
        print("constructing rej_dict for:", taxon)
        b_sheet = taxon + '-b-p'
        b_df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
        w_df = w_dfs[taxons.index(taxon)]

        correct_stat = [0]*alpha_num
        reject_stat = [0]*alpha_num
        total_count = 0

        # compute correct_stat, reject_stat, total, probs
        probs = []
        for index, row in b_df.iterrows():
            if row['prediction'] == taxon:
                total_count += 1
                reject_start = math.floor(row['max']*1/gap)/(1/gap)+gap
                reject_incre = [0]*(int(reject_start*1/gap))
                reject_incre.extend([1]*(int(alpha_num-reject_start*1/gap)))
                correct_incre = [1]*(int(reject_start*1/gap))
                correct_incre.extend([0]*(int(alpha_num-reject_start*1/gap)))
                correct_stat = [sum(x) for x in zip(correct_stat, correct_incre)]
                reject_stat = [sum(x) for x in zip(reject_stat, reject_incre)]
                probs.append(row['max'])
        for index, row in w_df.iterrows():
            total_count += 1
            reject_start = math.floor(row['max']*1/gap)/(1/gap)+gap
            reject_incre = [0]*(int(reject_start*1/gap))
            reject_incre.extend([1]*(int(alpha_num-reject_start*1/gap)))
            reject_stat = [sum(x) for x in zip(reject_stat, reject_incre)] 

        # compute thres_alpha
        thres_alpha = 1
        for correct_count, reject_count, alpha in zip(correct_stat, reject_stat, alphas):
            precision = 1 # if we have rejected all instances, precision = 1
            if (total_count-reject_count) != 0: 
                precision = correct_count/(total_count-reject_count)
            if precision >= accepted_CA:
                thres_alpha = alpha
                break
        if len(probs) != 0:
            thres_alpha = max(statistics.mean(probs)-variability, thres_alpha-variability)
        print("finished rej_dict for:", taxon)
        return thres_alpha


    # write to rej_dict
    rej_dict = {} # rejection threshold by taxon
    p = Pool(10)
    all_thres = p.map(taxon_recall, taxons)
    for taxon, thres in zip(taxons, all_thres):
        rej_dict[taxon] = thres
    with open(rej_path, 'w') as f:
        json.dump(rej_dict, f) 
        


