import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os

# python3 precision_recall_b.py outputs/fft-o__Oscillospirales.xlsx

alphas = np.arange(0, 1.01, 0.01).tolist()
file_name = sys.argv[1]
taxon = sys.argv[2]

xls = pd.ExcelFile(file_name)
precision = []
recall = []
weighted = []

for alpha in alphas:
    reads = 0
    correct = 0
    unassigned = 0
    for sheet in xls.sheet_names:
        if sheet.endswith('-p'):
            df = pd.read_excel(file_name, sheet_name=sheet)
            df = df.loc[df['prediction'] == taxon]
            if df.shape[0] == 0:
                continue
            df['rejection-'+str(alpha)] = df.apply(lambda row: 'reject' if row['max'] < alpha else row['prediction'], axis=1)
            predicted = df['rejection-'+str(alpha)].tolist()
            reads += df.shape[0]
            unassigned += predicted.count('reject')
            if sheet.startswith(taxon):
                correct += predicted.count(taxon)
            
    p = 1
    if (reads-unassigned) != 0:
        p = correct/(reads-unassigned)
    r = correct/reads
    p_weight = 0.5
    w = p_weight*p+(1-p_weight)*r
    precision.append(p)
    recall.append(r)
    weighted.append(w)
    print("alpha =", alpha, "precision:", p, "recall:", r, "weighted:", w)



plt.xticks(alphas[::5],  rotation='vertical')
plt.xlabel("threshould")
plt.ylabel("precision/recall")
plt.plot(alphas, precision, 'o-', label="Precision", markersize=2)
plt.plot(alphas, recall, 'o-', label="Recall", markersize=2)
plt.plot(alphas, weighted, 'o-', label="Weighted", markersize=2)
plt.axhline(y=0.8, color='r', linestyle='-')
plt.legend()

plt.savefig(file_name[:-5]+'-'+taxon+'-pr.png')
# plt.show()


