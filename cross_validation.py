
# Dependencies
import random
import pickle
import statistics
import numpy as np

from Bio import SeqIO
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix
from helpers import getStats, plotDict, kmer_count, build_pipeline, plot_confusion_matrix, get_misclassified_entries, print_misclassified_entries
import sys
from helpers import entries_count

input_folder = sys.argv[1]

dest_folder = "p_files/"

filename = dest_folder+input_folder+'.p'

with open(filename, 'rb') as f:
    data = pickle.load(f)


def training(train_data, k, classifier):
    train_features = []
    train_labels = []

    for i in range(len(train_data)):
        train_features.append(kmer_count(train_data[i][1], k))
        train_labels.append(train_data[i][0])

    x = np.asarray(train_features).astype('float32')
    x = normalize(x, norm='l2', axis=1)
    y = np.asarray(train_labels)

    features = normalize(x, norm='l2', axis=1)
    subtypes = np.asarray(train_labels)

    # Run the classification Pipeline for this subset.
    pipeline = build_pipeline(4 ** k, classifier)
    pipeline.fit(features, subtypes)

    return pipeline


def testing(test_data, k, pipeline, print_entries = False):
    n_test = len(test_data)

    test_features = []
    test_labels = []

    for i in range(len(test_data)):
        test_features.append(kmer_count(test_data[i][1], k))
        test_labels.append(test_data[i][0])

    x = np.asarray(test_features).astype('float32')
    y = np.asarray(test_labels)

    test_features = normalize(x, norm='l2', axis=1)

    y_pred = pipeline.predict(test_features)
    cm = confusion_matrix(y, y_pred)
    if print_entries:
        print(cm)
        print("printing misclassified entries")
        print_misclassified_entries(cm)
    # print(get_misclassified_entries(y, y_pred))
    #plot_confusion_matrix(cm[:100][:100], test_labels[:100])

    return accuracy_score(y, y_pred)



k = 9
classifiers = ['linear-svm', 'poly-svm', 'rbf-svm', 'lda', 'KNN']

accuracies = {}
index = 0
fold = 10
step = int(len(data) / fold)
random.shuffle(data)

for classifier in classifiers:
    accuracies[classifier] = []

for i in range(fold):
    print(i)
    train = data[:index] + data[index + step:]
    test = data[index:index + step]
    index = index + step

    for classifier in classifiers:
        print_entries = False
        if classifier == "linear-svm": # linear-svm seems to do better than other classifiers
            print_entries = True
        print(classifier)
        pipeline = training(train, k, classifier)
        accuracies[classifier].append(testing(test, k, pipeline, print_entries))
        print(accuracies)
    print('**************************************************')

print(accuracies)
for classifier in classifiers:
    print('accuracy of ' + classifier + ': ' + str(statistics.mean(accuracies[classifier])))

print("********************misclassified entries summary*****************")
print(entries_count)

