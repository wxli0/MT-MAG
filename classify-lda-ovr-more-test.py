
# Dependencies
import random
import pickle
import statistics
import numpy as np
import xlsxwriter
import openpyxl
import pandas as pd
import os.path
import json

from Bio import SeqIO
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix
from helpers_new import getStats, plotDict, kmer_count, build_pipeline, plot_confusion_matrix, get_misclassified_entries, print_misclassified_entries
import sys
from helpers_new import entries_count
from classifyhelpers import testing, training, read_pfiles_more_test
from sklearn.calibration import CalibratedClassifierCV
from scipy.special import softmax
from math import exp

#e.g. python3 classify.py o__Bacteroidales_exclude_g__C941 g__C941_wrapper


def testing_lda(test_data, k, pipeline, train_folder, test_folder, print_entries = False):
    test_features, y_pred, test_ids, y = testing(test_data, k, pipeline)

    f_x = pipeline.decision_function(test_features)

    labels = list(set(pipeline.classes_))
    labels.sort()
    if len(labels) == 2:
        labels_copy = labels
        labels = [labels_copy[0]+'-'+labels_copy[1]]
        
    df = pd.DataFrame(f_x, columns=labels)
    df['prediction'] = y_pred
    df.index = test_ids

    path = 'outputs/lda-'+train_folder+'.xlsx'
    m = 'w'
    if os.path.isfile(path):
        m = 'a'

    test_folder_short = test_folder
    if test_folder.endswith('wrapper'):
        test_folder_short = test_folder_short[:-13]
    sheet_name = test_folder_short+'-b'

    with pd.ExcelWriter(path, engine="openpyxl", mode=m) as writer:  
        df.to_excel(writer, sheet_name = sheet_name[:31], index=True)
    writer.save()
    writer.close()

    # write probabilities
    f_p = pipeline.predict_proba(test_features)
    df_p = pd.DataFrame(f_p, columns=labels)
    df_p['prediction'] = y_pred
    df_p['max'] = np.max(df_p, axis=1)
    df_p.index = test_ids
    sheet_name = test_folder_short+'p-b'
    with pd.ExcelWriter(path, engine="openpyxl", mode='a') as writer:  
        df_p.to_excel(writer, sheet_name = sheet_name[:31], index=True)
    writer.save()
    writer.close()

    return accuracy_score(y, y_pred)


print('************ classify new sequences ************************')
np.set_printoptions(suppress=True)


train, tests = read_pfiles_more_test(sys.argv[1])

json_input = json.load(open(sys.argv[1]))
train_folder = json_input['train_folder']
test_folders = json_input['test_folders']

k = 7
classifier = 'lda'
print("training")
pipeline = training(train, k, classifier)
print("training done")

for test, test_folder in zip(tests, test_folders):
    print("testing", test_folder)
    acc = testing_lsvm(test, k, pipeline, train_folder, test_folder)
    print(classifier+":", acc)

