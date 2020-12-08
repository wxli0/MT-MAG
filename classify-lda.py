
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

def testing_lda(test_data, k, pipeline):
    test_features, y_pred, test_ids, y = testing(test_data, k, pipeline)

    probs = pipeline.predict_proba(test_features)
    labels = list(set(pipeline.classes_))
    labels.sort()
    df = pd.DataFrame(probs, columns=labels)
    df['prediction'] = y_pred
    df.index = test_ids

    path = 'outputs/fft-'+train_folder+'.xlsx'
    m = 'w'
    if os.path.isfile(path):
        m = 'a'
    with pd.ExcelWriter(path, engine="openpyxl", mode=m) as writer:  
        df.to_excel(writer, sheet_name = test_folder+'-'+pipeline.prefix+'p', index=True)
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
classifier = 'lda'
pipeline = training(train, k, classifier)
acc = testing_lda(test, k, pipeline)
print(classifier+":", acc)

