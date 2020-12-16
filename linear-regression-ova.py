
# Dependencies
import random
import pickle
import statistics
import numpy as np
import xlsxwriter
import openpyxl
import pandas as pd
import os.path
import torch
import math

from Bio import SeqIO
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix
from helpers import getStats, plotDict, kmer_count, build_pipeline, plot_confusion_matrix, get_misclassified_entries, print_misclassified_entries
import sys
from helpers import entries_count
from sklearn import preprocessing
from classifyhelpers import testing, training, read_pfiles



import torch
from torch.autograd import Variable
class linearRegression(torch.nn.Module):
    def __init__(self, inputSize, outputSize):
        super(linearRegression, self).__init__()
        self.linear = torch.nn.Linear(inputSize, outputSize)

    def forward(self, x):
        out = self.linear(x)
        return out

# least square loss
def ls(r):
    return (1-r)**2


def dot_product(v1, v2):
    return sum([x*y for x,y in zip(v1,v2)])


def training_autograd(train_data, k):
    train_features = []
    train_labels = []

    for i in range(len(train_data)):
        train_features.append(kmer_count(train_data[i][1], k))
        train_labels.append(train_data[i][0])

    x = np.asarray(train_features).astype('float32')
    # x = normalize(x, norm='l2', axis=1)
    y = np.asarray(train_labels)

    # features = normalize(x, norm='l2', axis=1)
    x_train = np.abs(np.fft.fft(x))
    y_train = np.asarray(train_labels)
    print("y_train before:", y_train)
    y_unique = np.unique(y_train)
    y_unique.sort()
    y_classes_num = len(y_unique)

    print("y_unique is:", y_unique)
    le = preprocessing.LabelEncoder()
    y_train = le.fit_transform(y_train)
    y_unique = np.unique(y_train)
    y_unique.sort()
    y_classes_num = len(y_unique)
    print("y_unique after is:", y_unique)


    inputDim = x_train.shape[1]        # takes variable 'x' 
    outputDim = 1       # takes variable 'y'
    learningRate = 0.00001 
    epochs = 1000

    def OVA_loss(outputs, labels):
        loss = 0
        for i in range(len(labels)):
            for j in range(y_classes_num):
                if y_unique[j] == labels[i]:
                    loss += ls(outputs[j][i])
                else:
                    loss += ls(-outputs[j][i])
        return loss

    models = []
    for i in range(y_classes_num):
        models.append(linearRegression(inputDim, outputDim))

    if torch.cuda.is_available():
        for m in models:
            m.cuda()

    optimizers = []
    for m in models:
        optimizers.append(torch.optim.SGD(m.parameters(), lr=learningRate))

    for epoch in range(epochs):
        # Converting inputs and labels to Variable
        if torch.cuda.is_available():
            inputs = Variable(torch.from_numpy(x_train).cuda())
            labels = Variable(torch.from_numpy(y_train).cuda())
        else:
            inputs = Variable(torch.from_numpy(x_train))
            labels = Variable(torch.from_numpy(y_train))

        # Clear gradient buffers because we don't want any gradient from previous epoch to carry forward, dont want to cummulate gradients
        for o in optimizers:
            o.zero_grad()

        # get output from the model, given the inputs
        outputs = []
        for m in models:
            outputs.append(m(inputs.float()))

        # get loss for the predicted output
        loss = OVA_loss(outputs, labels)
        print(loss)
        # get gradients w.r.t to parameters
        loss.backward()

        # update parameters
        for o in optimizers:
            o.step()

        print('epoch {}, loss {}'.format(epoch, loss.item()))


print('************ classify new sequences ************************')
np.set_printoptions(suppress=True)
train_folder = sys.argv[1]
test_folder = sys.argv[2]

dest_folder = "p_files/"

train_filename = dest_folder+train_folder+'.p'
test_filename = dest_folder+test_folder+'.p'

train, test = read_pfiles(train_filename, test_filename)

k = 7


training_autograd(train, k)

