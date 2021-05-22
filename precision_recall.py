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

xls = pd.ExcelFile(file_name)
precision = []
recall = []
weighted = []

excel_alpha_info = {}
alpha_num = (1+gap)/gap+1

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
            print("reach adding to w_df")
            print(row)
            w_dfs[taxons.index(pred)].loc[index] = row
            print(w_dfs[taxons.index(pred)])

print("print w_dfs")
print(w_dfs)


# calculating excel_alpha_info
print("calculating excel_alpha_info")
for taxon in taxons:
    b_sheet = taxon + '-b-p'
    df = pd.read_excel(file_name, sheet_name=b_sheet, index_col=0, header=0)
    sheet_alpha_info = []
    for index, row in df.iterrows():
        round_down_max = math.floor(row['max']*100)/100.0
        pred_num = round_down_max/gap
        true_half = [True]*(int(pred_num))
        true_half.extend([False]*int((alpha_num-pred_num)))
        excel_alpha_info[index] =  true_half

rej_dict = {} # precision threshold by taxon

print("constructing rej_dict")
for taxon in taxons:
    print("constructing rej_dict for:", taxon)
    b_sheet = taxon + '-b-p'
    precisions = []
    recalls = []
    done = False
    thres_alpha = 0
    probs = []
    for alpha in alphas:
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
            elif row['prediction'] == taxon:
                correct_count += 1
                probs.append(row['max'])
        for index, row in w_df.iterrows():
            row_alpha_info = excel_alpha_info[index]
            if not row_alpha_info[int(alpha/gap)]:
                reject_count += 1
        p = 1
        if (read_count-reject_count) != 0:
            p = correct_count/(read_count-reject_count)
        if not done and p > 0.9:
            thres_alpha = p
            done = True
        precisions.append(p)
        r = correct_count/read_count
        recalls.append(r)
    thres_alpha = max(statistics.mean(probs)-0.2, thres_alpha-0.2)
    rej_dict[taxon] = thres_alpha
    
    plt.figure(taxon)
    plt.xticks(alphas[::5],  rotation='vertical')
    plt.xlabel("threshould")
    plt.ylabel("precision/recall")
    plt.plot(alphas, precisions, 'o-', label="Precision", markersize=2)
    plt.plot(alphas, recalls, 'o-', label="Recall", markersize=2)
    plt.axhline(y=0.9, color='r', linestyle='-')
    plt.legend()
    plt.savefig(file_name[:-5]+'-'+taxon+'-pr.png')

ver = file_name.split('/')[0].split('-')[-1]
BK_path = "/Users/wanxinli/Desktop/project/BlindKameris-new/rejection-threshold-"+ver+"/"
if platform.platform()[:5] == 'Linux':
    BK_path = "/home/w328li/BlindKameris-new/rejection-threshold-"+ver+"/"
if platform.node() == 'q.vector.local' or platform.node().startswith('guppy'):
    BK_path = "/h/wanxinli/BlindKameris-new/rejection-threshold-"+ver+"/"

rej_path = BK_path+file_name.split('/')[-1][:-11]+'.json'

if not os.path.isfile(rej_path):
    with open(rej_path, 'w') as f:
        json.dump(rej_dict, f)

