
# Dependencies
import random
import pickle
import statistics
import numpy as np

from Bio import SeqIO
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix
from helpers import getStats, plotDict, kmer_count, build_pipeline, plot_confusion_matrix
import sys

input_folder = sys.argv[1]

dest_folder = "p_files/"

filename = dest_folder+input_folder+'.p'

with open(filename, 'rb') as f:
    data = pickle.load(f)

print(len(data))


unique_labels = list(set(map(lambda x: x[0], data)))

#get some stats about training and testing dataset
diTrain = getStats(data)
plotDict(diTrain, 'train.png',"Order_Barcode")

# Create Labels for Classes
diLabels = {}
classId = 0;
numClasses = len(diTrain)

for item in diTrain:
    classId += 1
    diLabels[item] = classId;

print(diLabels)

# Select the minimun amount of elements per class
minimum = 25

# Create Labels for Classes
diLabels = {}
classId = 0;
numClasses = len(diTrain)

i = 0
while i < len(data):
    if diTrain[data[i][0]] < minimum:
        data.pop(i)
    else:
        i+=1

# Select the maximum amount of elements per class
maximum = 3000

i = 0
overrepresented_classes = []
while i < len(data):
    if diTrain[data[i][0]] > maximum:
        if labels[i] not in overrepresented_classes:
            overrepresented_classes.append(labels[i])
    i+=1

delete = False
for label in overrepresented_classes:
    count = 0
    i = 0
    while i < len(data):
        if count == maximum:
            delete = True
        if labels[i] == label:
            if not delete:
                count += 1
                i += 1
            else:
                data.pop(i)
                sequences.pop(i)
                labels.pop(i)
        else:
            i += 1

# get some stats about the training dataset
diTrain = getStats(data)
plotDict(diTrain, 'virus-families.png','Virus Families')
print(diTrain)


# 70% of data for training and 30% for testing
ratio = 0.7
len_train_data = int(len(data) * ratio)

random.shuffle(data)

train = data[:len_train_data]
test = data[len_train_data:]

#Change the path to your convenience.

with open('train.p', 'wb') as f:
    pickle.dump(train, f)

with open('test.p', 'wb') as f:
    pickle.dump(test, f)

k = 9  # Select the value of k that you want to use.


unique_labels = list(set(map(lambda x: x[0], train)))

#get some stats about training and testing dataset
diTrain = getStats(train)
plotDict(diTrain, 'train.png',"Virus Families")

# Create Labels for Classes
diLabels = {}
classId = 0;
numClasses = len(diTrain)

for item in diTrain:
    classId += 1
    diLabels[item] = classId;

print(diLabels)


n_train = len(train)
train_features = []
train_labels = []

for i in range(len(train)):
    train_features.append(kmer_count(train[i][1], k))
    train_labels.append(train[i][0])

x = np.asarray(train_features).astype('float32')
y = np.asarray(train_labels)


features = normalize(x, norm='l2',axis=1)
subtypes = np.asarray(train_labels)


print(features.shape)

# Run the classification Pipeline for this subset.
# Here you have the freedom to select your favorite classifier.
# You don't have to follow our pipeline. You can add a CNN or
# a MLP.

pipeline = build_pipeline(4**k, 'poly-svm')
pipeline.fit(features, subtypes)


n_test = len(test)

test_features = []
test_labels = []

for i in range(len(test)):
    test_features.append(kmer_count(test[i][1], k))
    test_labels.append(test[i][0])

x = np.asarray(test_features).astype('float32')
y = np.asarray(test_labels)


test_features = normalize(x, norm = 'l2', axis = 1)


#get some stats about the testing dataset
diTrain = getStats(test)
plotDict(diTrain, 'test.png','Virus Families')
print(diTrain)


y_pred = pipeline.predict(test_features)
print(accuracy_score(y, y_pred))


def training(train_data, k, classifier):
    n_train = len(train_data)
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


def testing(test_data, k, pipeline):
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
    print(cm)
    #plot_confusion_matrix(cm[:100][:100], test_labels[:100])

    return accuracy_score(y, y_pred)



k = 9
classifiers = ['linear-svm', 'poly-svm', 'rbf-svm', 'LinearDiscriminant', 'KNN']

accuracies = {}
index = 0
step = int(len(data) / 10)
random.shuffle(data)

for classifier in classifiers:
    accuracies[classifier] = []

for i in range(10):
    print(i)
    train = data[:index] + data[index + step:]
    test = data[index:index + step]
    index = index + step

    for classifier in classifiers:
        print(classifier)
        pipeline = training(train, k, classifier)
        accuracies[classifier].append(testing(test, k, pipeline))
        print(accuracies)
    print('**************************************************')

print(accuracies)
for classifier in classifiers:
    print('accuracy of ' + classifier + ': ' + str(statistics.mean(accuracies[classifier])))



