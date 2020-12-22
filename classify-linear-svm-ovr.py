
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
from helpers_new import getStats, plotDict, kmer_count, build_pipeline, plot_confusion_matrix, get_misclassified_entries, print_misclassified_entries
import sys
from helpers_new import entries_count
from classifyhelpers import testing, training, read_pfiles
from sklearn.calibration import CalibratedClassifierCV
from scipy.special import softmax
from math import exp

#e.g. python3 classify.py o__Bacteroidales_exclude_g__C941 g__C941_wrapper

def f_to_c(theta):
    return -2*max(0, 1+theta)/(-2*max(0, 1+theta)-2*max(0, 1-theta))


def custom_softmax(f_x):
    alpha = 1.4
    ret = np.zeros(f_x.shape)
    for j in range(f_x.shape[0]):
        r = f_x[j]
        # print("r is:", r)
        nor_r = np.zeros(f_x.shape[1])
        for i in range(len(r)):
            nor_r[i] = alpha*exp(r[i])
            if r[i] < 0:
                nor_r[i] = exp(r[i])
            nor_r /= np.sum(nor_r)
        # print("nor_r is:", nor_r)
        ret[j] = nor_r
    return ret


def testing_lsvm(test_data, k, pipeline, print_entries = False):
    test_features, y_pred, test_ids, y = testing(test_data, k, pipeline)

    f_x = pipeline.decision_function(test_features)
    f_post1 = softmax(f_x, axis=1)
    # f_post = pipeline.predict_proba(test_features)
    f_post = custom_softmax(f_x)
    f_to_c_vec = np.vectorize(f_to_c)
    f_x_c = f_to_c_vec(f_x)
    labels = list(set(pipeline.classes_))
    labels.sort()
    if len(labels) == 2:
        labels_copy = labels
        labels = [labels_copy[0]+'-'+labels_copy[1]]
        
    df = pd.DataFrame(f_x, columns=labels)
    df['prediction'] = y_pred
    df.index = test_ids

    df_post = pd.DataFrame(f_post, columns=labels)
    df_post.index = test_ids
    df_post['max'] = np.max(f_post, axis=1)
    df_post['prediction'] = y_pred

    df_post1 = pd.DataFrame(f_post1, columns=labels)
    df_post1.index = test_ids
    df_post1['max'] = np.max(f_post1, axis=1)
    df_post1['prediction'] = y_pred
    
    df_c = pd.DataFrame(f_x_c, columns=labels)
    df_c['prediction'] = y_pred
    df_c.index = test_ids
    print("using softmax")
    print(df_post1)

    print("using custom softmax")
    print(df_post)

    path = 'outputs/fft-'+train_folder+'.xlsx'
    m = 'w'
    if os.path.isfile(path):
        m = 'a'

    test_folder_short = test_folder
    if test_folder.endswith('wrapper'):
        test_folder_short = test_folder_short[:-8]
    sheet_name = test_folder_short+'-'+pipeline.prefix

    with pd.ExcelWriter(path, engine="openpyxl", mode=m) as writer:  
        df.to_excel(writer, sheet_name = sheet_name[:31], index=True)
    writer.save()
    writer.close()
    
    # with pd.ExcelWriter(path, engine="openpyxl", mode='a') as writer:  
    #     df_c.to_excel(writer, sheet_name = sheet_name[:29]+'-c', index=True)
    # writer.save()
    # writer.close()

    # with pd.ExcelWriter(path, engine="openpyxl", mode='a') as writer:  
    #     df_post1.to_excel(writer, sheet_name = sheet_name[:29]+'-l', index=True)
    # writer.save()
    # writer.close()

    with pd.ExcelWriter(path, engine="openpyxl", mode='a') as writer:  
        df_post.to_excel(writer, sheet_name = sheet_name[:29]+'-cl', index=True)
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
classifier = 'linear-svm'
pipeline = training(train, k, classifier)
acc = testing_lsvm(test, k, pipeline)
print(classifier+":", acc)

