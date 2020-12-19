# Dependencies
import numpy as np
from helpers_new import getStats, plotDict, kmer_count, build_pipeline, plot_confusion_matrix, get_misclassified_entries, print_misclassified_entries
import sys
from helpers_new import entries_count
import pickle

def testing(test_data, k, pipeline):
    test_features = []
    test_labels = []
    test_ids = []

    for i in range(len(test_data)):
        test_features.append(kmer_count(test_data[i][1], k))
        test_labels.append(test_data[i][0])
        test_ids.append(test_data[i][2])

    x = np.asarray(test_features).astype('float32')
    y = np.asarray(test_labels)

    # test_features = normalize(x, norm='l2', axis=1)
    test_features = np.abs(np.fft.fft(x))

    y_pred = pipeline.predict(test_features)
    return test_features, y_pred, test_ids, y


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
    if classifier == 'linear-svm':
        pipeline.prefix = 'LSVM'
    if classifier == 'linear-svm-ovo':
        pipeline.prefix = 'LSVM-ovo'
    elif classifier == 'lda':
        pipeline.prefix = 'LDA'
    elif classifier == 'quadratic-svm':
        pipeline.prefix = 'QSVM'

    return pipeline

def read_pfiles(train_filename, test_filename):
    with open(train_filename, 'rb') as f:
        train = pickle.load(f)
    with open(test_filename, 'rb') as f:
        test = pickle.load(f)
    return train, test