import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# python3 precision_recall_b.py outputs/fft-o__Oscillospirales.xlsx

alphas = np.arange(0, 1.02, 0.02).tolist()
file_name = sys.argv[1]

xls = pd.ExcelFile(file_name)
precision = []
recall = []

for alpha in alphas:
    reads = 0
    correct = 0
    unassigned = 0
    for sheet in xls.sheet_names:
        if sheet.endswith('-b'):
            print("processing", sheet)
            df = pd.read_excel(file_name, sheet_name=sheet)
            df['rejection-'+str(alpha)] = df.apply(lambda row: 'reject' if row['max'] < alpha else row['prediction'], axis=1)
            predicted = df['rejection-'+str(alpha)].tolist()
            reads += len(predicted)
            unassigned += predicted.count('reject')
            correct += predicted.count(sheet[:-2])
    p = correct/(reads-unassigned)
    r = correct/reads
    precision.append(p)
    recall.append(r)
    print("alpha =", alpha, "precision:", p, "recall:", r)



plt.xticks(alphas[::5],  rotation='vertical')
plt.xlabel("threshould")
plt.ylabel("precision/recall")
plt.plot(alphas, precision, 'o-', label="Precision", markersize=5)
plt.plot(alphas, recall, 'o-', label="Recall", markersize=5)
plt.legend()
plt.savefig(file_name[:-5]+'-pr.png')
plt.show()

