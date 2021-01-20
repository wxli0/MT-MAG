import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import json

# python3 precision_recall_b.py outputs/fft-o__Oscillospirales.xlsx

alphas = np.arange(0, 1.02, 0.02).tolist()
file_name = sys.argv[1]
label_dict = json.load(open(sys.argv[2]))

xls = pd.ExcelFile(file_name)
precision = []
recall = []
weighted = []


for alpha in alphas:
    reads = 0
    correct = 0
    unassigned = 0
    for sheet in xls.sheet_names:
        if sheet.endswith('-t'):
            print("processing", sheet)
            df = pd.read_excel(file_name, sheet_name=sheet)
            df['rejection-'+str(alpha)] = df.apply(lambda row: 'reject' if row['max'] < alpha else row['prediction'], axis=1)
            predicted = df['rejection-'+str(alpha)].tolist()
            reads += len(predicted)
            true_label = label_dict[sheet[:-2]]
            unassigned += predicted.count('reject')
            correct += predicted.count(true_label)
    p = 1
    if (reads-unassigned) != 0:
        p = correct/(reads-unassigned)
    r = correct/reads
    w = 0.5*p+0.5*r
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
# plt.axhline(y=0.75, color='r', linestyle='-')
plt.legend()
plt.savefig(file_name[:-5]+'-t-pr.png')
plt.show()

