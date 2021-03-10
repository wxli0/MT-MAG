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

# python3 precision_recall_b.py outputs/fft-o__Oscillospirales.xlsx

gap = 0.01
alphas = np.arange(0, 1+gap, gap).tolist()
file_name = sys.argv[1]
taxon = sys.argv[2]

xls = pd.ExcelFile(file_name)
precision = []
recall = []
weighted = []

excel_alpha_info = {}
alpha_num = (1+gap)/gap+1

print("enter 1")
for sheet in xls.sheet_names:
    print("sheet is:", sheet)
    if sheet.endswith('-p'):
        df = pd.read_excel(file_name, sheet_name=sheet, index_col=0, header=0)
        sheet_alpha_info = []
        for index, row in df.iterrows():
            print("index adding is:", index)
            round_down_max = math.floor(row['max']*100)/100.0
            pred_num = round_down_max/gap
            true_half = [True]*(int(pred_num))
            true_half.extend([False]*int((alpha_num-pred_num)))
            print("here:", true_half.extend([False]*int((alpha_num-pred_num))))
            excel_alpha_info[index] =  true_half


print("enter 2")
print("excel_alpha_info is:", excel_alpha_info)
thres_alpha = 0
done = 0
for alpha in alphas:
    reads = 0
    correct = 0
    unassigned = 0
    for sheet in xls.sheet_names:
        print("sheet_name is:", sheet)
        if sheet.endswith('-p'):
            df = pd.read_excel(file_name, sheet_name=sheet, index_col=0, header=0)
            df = df.loc[df['prediction'] == taxon]
            if df.shape[0] == 0:
                continue
            predicted = []
            for index, row in df.iterrows():
                print("index is:", index)
                row_alpha_info = excel_alpha_info[index]
                print("enter2")
                print("pred is:", row_alpha_info)
                one_predicted = row['prediction'] if row_alpha_info[int(alpha/gap)] else 'reject'
                predicted.append(one_predicted)
                print("one_predicted is:", one_predicted)
            reads += df.shape[0]
            unassigned += predicted.count('reject')
            if sheet.startswith(taxon):
                print("final predicted is:", predicted)
                correct += predicted.count(taxon)
    p = 1
    if (reads-unassigned) != 0:
        p = correct/(reads-unassigned)
    r = correct/reads
    p_weight = 0.5
    w = p_weight*p+(1-p_weight)*r
    precision.append(p)
    if not done and p > 0.95:
        thres_alpha = alpha
        done = True
    recall.append(r)
    weighted.append(w)
    print("alpha =", alpha, "precision:", p, "recall:", r, "weighted:", w)    


plt.xticks(alphas[::5],  rotation='vertical')
plt.xlabel("threshould")
plt.ylabel("precision/recall")
plt.plot(alphas, precision, 'o-', label="Precision", markersize=2)
plt.plot(alphas, recall, 'o-', label="Recall", markersize=2)
plt.plot(alphas, weighted, 'o-', label="Weighted", markersize=2)
plt.axhline(y=0.7, color='r', linestyle='-')
plt.legend()

plt.savefig(file_name[:-5]+'-'+taxon+'-pr.png')
# plt.show()

BK_path = "/Users/wanxinli/Desktop/project/BlindKameris-new/rejection_threshold/"
if platform.platform()[:5] == 'Linux':
    BK_path = "/home/w328li/BlindKameris-new/rejection_threshold/"
if platform.node() == 'q.vector.local' or platform.node().startswith == 'guppy':
    BK_path = "/h/wanxinli/BlindKameris-new/rejection_threshold/"

print("file name is:", file_name)
print("split results is:", file_name.split('/'))
rej_path = BK_path+file_name.split('/')[-1][:-11]+'.json'

if not os.path.isfile(rej_path):
    rej_dict = {taxon: thres_alpha}
    with open(rej_path, 'w') as f:
        json.dump(rej_dict, f)
else:
    with open(rej_path) as json_file:
        rej_dict = json.load(json_file)
        rej_dict[taxon] = thres_alpha

    with open(rej_path, 'w') as json_file:
        json.dump(rej_dict, json_file)



