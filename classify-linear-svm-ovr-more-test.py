
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

def f_to_c(theta):
    return -2*max(0, 1+theta)/(-2*max(0, 1+theta)-2*max(0, 1-theta))


def custom_softmax(f_x):
    alpha = 1.2
    ret = np.zeros(f_x.shape)
    for j in range(f_x.shape[0]):
        r = f_x[j]
        # print("r is:", r)
        nor_r = np.zeros(f_x.shape[1])
        for i in range(len(r)):
            nor_r[i] = alpha*exp(r[i])
            if r[i] > 0:
                nor_r[i] = exp(r[i])
        nor_r /= np.sum(nor_r)
        # print("nor_r is:", nor_r)
        ret[j] = nor_r
    return ret


def testing_lsvm(test_data, k, pipeline, train_folder, test_folder, print_entries = False):
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

    path = 'outputs/'+train_folder+'.xlsx'
    m = 'w'
    if os.path.isfile(path):
        m = 'a'

    test_folder_short = test_folder
    if test_folder.endswith('_eval_wrapper'):
        test_folder_short = test_folder_short[:-13]
        test_folder_short = test_folder_short.split('/')[-1]
        sheet_name = test_folder_short+'-b'
    elif test_folder.endswith('_test_wrapper'):
        test_folder_short = test_folder_short[:-13]
        test_folder_short = test_folder_short.split('/')[-1]
        sheet_name = test_folder_short+'-t'
    elif test_folder_short.endswith("_wrapper"):
        test_folder_short = test_folder_short[:-8]
        test_folder_short = test_folder_short.split('/')[-1]
        sheet_name = test_folder_short+'-t'
    else:
        sheet_name = test_folder_short.split('/')[-1]

    print("sheet_name is:", sheet_name)
    with pd.ExcelWriter(path, engine="openpyxl", mode=m) as writer:  
        df.to_excel(writer, sheet_name = sheet_name[:31], index=True)
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
classifier = 'linear-svm'
print("training")
pipeline = training(train, k, classifier)
print("training done")

for test, test_folder in zip(tests, test_folders):
    print("testing", test_folder)
    acc = testing_lsvm(test, k, pipeline, train_folder, test_folder)
    print(classifier+":", acc)

