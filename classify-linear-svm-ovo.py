
# Dependencies
import random
import pickle
import statistics
import numpy as np
import xlsxwriter
import openpyxl
import pandas as pd
import os.path

from Bio import SeqIO
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix
from helpers import getStats, plotDict, kmer_count, build_pipeline, plot_confusion_matrix, get_misclassified_entries, print_misclassified_entries
import sys
from helpers import entries_count
from classifyhelpers import testing, training, read_pfiles

#e.g. python3 classify.py o__Bacteroidales_exclude_g__C941 g__C941_wrapper



def testing_lsvm_ovo(test_data, k, pipeline, print_entries = False):
    test_features, y_pred, test_ids, y = testing(test_data, k, pipeline)
    f_x = pipeline.decision_function(test_features)
    labels = list(set(pipeline.classes_))
    labels.sort()
    pair_labels = []
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            pair_labels.append(labels[i]+'-'+labels[j])

    df = pd.DataFrame(f_x, columns=pair_labels)
    df['prediction'] = y_pred
    df.index = test_ids
    print(df)

    path = 'outputs/fft-'+train_folder+'.xlsx'
    m = 'w'
    if os.path.isfile(path):
        m = 'a'
    test_folder_short = test_folder
    if test_folder.endswith('wrapper'):
        test_folder_short = test_folder_short[:-7]
    sheet_name = test_folder_short+'-'+pipeline.prefix
    with pd.ExcelWriter(path, engine="openpyxl", mode=m) as writer:  
        df.to_excel(writer, sheet_name = sheet_name[:31], index=True)
    writer.save()
    writer.close()

    return accuracy_score(y, y_pred)


print('************ classify new sequences ************************')
np.set_printoptions(suppress=True)
train_folder = sys.argv[1]
test_folder = sys.argv[2]

dest_folder = "p_files/"

train_filename = dest_folder+train_folder+'.p'
test_filename = dest_folder+test_folder+'.p'

train, test = read_pfiles(train_filename, test_filename)

k = 7
classifier = 'linear-svm-ovo'
pipeline = training(train, k, classifier)
acc = testing_lsvm_ovo(test, k, pipeline)
print(classifier+":", acc)

