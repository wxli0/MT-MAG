import sys
import numpy as np 
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import shutil
import json 
import platform
import math
import statistics

# python3 precision_recall.py outputs/fft-o__Oscillospirales.xlsx

gap = 0.01
alphas = np.arange(0, 1+gap, gap).tolist()
file_name = sys.argv[1]
test_file = sys.argv[2]
data_type = sys.argv[3]

xls = pd.ExcelFile(file_name)
precision = []
recall = []
weighted = []

excel_alpha_info = {}
alpha_num = 1/gap+1

taxons = [x[:-4] for x in xls.sheet_names]

w_dfs = []
for taxon in taxons:
    b_sheet = taxon + '-b-p'
    b_df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
    tmp_col = ['Row']
    tmp_col.extend(b_df.columns)
    w_df = pd.DataFrame(columns=tmp_col)
    w_df = w_df.set_index('Row')
    w_dfs.append(w_df)

# construct w_dfs
print("constructing dfs")
for taxon in taxons:
    print("construct df for:", taxon)
    b_sheet = taxon + '-b-p'
    b_df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
    for index, row in b_df.iterrows():
        pred = row['prediction']
        if pred != taxon: # add to w_df
            # print(row)
            w_dfs[taxons.index(pred)].loc[index] = row
            # print(w_dfs[taxons.index(pred)])

# print("print w_dfs")
# print(w_dfs)

# read in test file
test_df = pd.read_excel(test_file, sheet_name = 'quadratic-svm-score', header=0, index_col=0)
existing_preds = list(set(test_df['prediction']))
for i in range(len(existing_preds)):
    existing_preds[i] = int(existing_preds[i])-1

# calculating excel_alpha_info
print("calculating excel_alpha_info")
for taxon in taxons:
    b_sheet = taxon + '-b-p'
    df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
    sheet_alpha_info = []
    for index, row in df.iterrows():
        round_down_max = math.floor(row['max']*100)/100.0
        pred_num = round_down_max/gap+1
        true_half = [True]*(int(pred_num))
        true_half.extend([False]*int((alpha_num-pred_num)))
        excel_alpha_info[index] =  true_half

ver = file_name.split('/')[0].split('-')[-1]
BK_path = "/Users/wanxinli/Desktop/project/BlindKameris-new/rejection-threshold-"+data_type+ver+"/"
if platform.platform()[:5] == 'Linux':
    BK_path = "/home/w328li/BlindKameris-new/rejection-threshold-"+data_type+"-"+ver+"/"
if platform.node() == 'q.vector.local' or platform.node().startswith('guppy'):
    BK_path = "/h/wanxinli/BlindKameris-new/rejection-threshold-"+data_type+"-"+ver+"/"

rej_dict = {} # precision threshold by taxon
rej_path = BK_path+file_name.split('/')[-1][:-11]+'.json'

print("constructing rej_dict")
for taxon in taxons:
    if os.path.exists(rej_path):
        rej_dict = json.load(open(rej_path))
        if taxon in rej_dict:
            print(taxon, "already in rej_dict")
            continue     
    taxon_index = taxons.index(taxon)
    if taxon_index not in existing_preds:
        print(taxon, "not in existing_preds")
        continue
    print("constructing rej_dict for:", taxon)
    b_sheet = taxon + '-b-p'
    probs = []
    for alpha in alphas:
        probs = []
        thres_alpha = 1
        correct_count = 0
        reject_count = 0
        b_df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
        w_df = w_dfs[taxons.index(taxon)]
        read_count = w_df.shape[0]
        for index, row in b_df.iterrows():
            if row['prediction'] != taxon:
                continue
            read_count += 1
            row_alpha_info = excel_alpha_info[index]
            if not row_alpha_info[int(alpha/gap)]:
                reject_count += 1
            elif row['prediction'] == taxon: # index that are correctly classified to be taxon
                correct_count += 1
                probs.append(row['max'])
        for index, row in w_df.iterrows():
            row_alpha_info = excel_alpha_info[index]
            if not row_alpha_info[int(alpha/gap)]:
                reject_count += 1
        p = 1
        if (read_count-reject_count) != 0: # not all are rejected
            p = correct_count/(read_count-reject_count)
        if p > 0.9:
            thres_alpha = alpha
            break
    if correct_count == 0:
        thres_alpha = 1 # no instances are classified correctly to taxon
    else:
        thres_alpha = max(statistics.mean(probs)-0.2, thres_alpha-0.2)
    rej_dict[taxon] = thres_alpha
    with open(rej_path, 'w') as f:
        json.dump(rej_dict, f)
    

rej_path = BK_path+file_name.split('/')[-1][:-11]+'.json'

if not os.path.isfile(rej_path):
    with open(rej_path, 'w') as f:
        json.dump(rej_dict, f)


