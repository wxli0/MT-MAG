
# Dependencies
import random
import pickle
import statistics
import numpy as np
import xlsxwriter
import openpyxl
import pandas as pd

from Bio import SeqIO
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix
from helpers import getStats, plotDict, kmer_count, build_pipeline, plot_confusion_matrix, get_misclassified_entries, print_misclassified_entries
import sys
from helpers import entries_count

#e.g. python3 classify.py o__Bacteroidales_exclude_g__C941 g__C941_wrapper

np.set_printoptions(suppress=True)
train_folder = sys.argv[1]
test_folder = sys.argv[2]

dest_folder = "p_files/"

train_filename = dest_folder+train_folder+'.p'
test_filename = dest_folder+test_folder+'.p'

with open(train_filename, 'rb') as f:
    train = pickle.load(f)

with open(test_filename, 'rb') as f:
    test = pickle.load(f)

def training(train_data, k, classifier):
    train_features = []
    train_labels = []

    for i in range(len(train_data)):
        train_features.append(kmer_count(train_data[i][1], k))
        train_labels.append(train_data[i][0])

    x = np.asarray(train_features).astype('float32')
    # x = normalize(x, norm='l2', axis=1)
    y = np.asarray(train_labels)

    # features = normalize(x, norm='l2', axis=1)
    features = np.abs(np.fft.fft(x))
    subtypes = np.asarray(train_labels)

    # Run the classification Pipeline for this subset.
    pipeline = build_pipeline(4 ** k, classifier)
    pipeline.fit(features, subtypes)

    return pipeline


def testing(test_data, k, pipeline, print_entries = False):
    test_features = []
    test_labels = []

    for i in range(len(test_data)):
        test_features.append(kmer_count(test_data[i][1], k))
        test_labels.append(test_data[i][0])

    x = np.asarray(test_features).astype('float32')
    y = np.asarray(test_labels)

    # test_features = normalize(x, norm='l2', axis=1)
    test_features = np.abs(np.fft.fft(x))

    y_pred = pipeline.predict(test_features)
    print("y is:", y)
    print("y_pred is:", y_pred)
    cm = confusion_matrix(y, y_pred)
    if print_entries:
        print(cm)
        print("printing misclassified entries")
        print_misclassified_entries(cm)

    f_x = pipeline.decision_function(test_features)
    df = pd.DataFrame(f_x, columns=list(set(pipeline.classes_)))
    print(df)
    path = 'outputs/fft-'+train_folder+'.xlsx'
    with pd.ExcelWriter(path, engine="openpyxl", mode='a') as writer:  
        df.to_excel(writer, sheet_name = test_folder+'-SH', index=False)
    writer.save()
    writer.close()

    return accuracy_score(y, y_pred)


print('************ classify new sequences ************************')

k = 7
# classifiers = ['linear-svm', 'poly-svm', 'rbf-svm', 'LinearDiscriminant', 'KNN']
classifiers = ['linear-svm']


for classifier in classifiers:
    pipeline = training(train, k, classifier)
    acc = testing(test, k, pipeline)
    print(classifier+":", acc)



