import pandas as pd

from autograd import grad
from autograd import elementwise_grad
import autograd.numpy as np

X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
x1 = np.ones((X.shape[0], 1))
# X = np.concatenate((x1, X), axis=1)
y = np.dot(X, np.array([1, 2])) + 3

weights = np.zeros(X.shape[1])
eps = 1e-15

def wTx(w, x):
    return np.dot(x, w)


def lr_predictions(w, x):
    predictions = wTx(w, x)
    return predictions

def custom_loss(y, y_predicted):
    print("y is:", y)
    print("y_predicted is:", y_predicted)
    # return -((1-y*y_predicted)**2).mean()
    return -((y-y_predicted)**2).mean()

def custom_loss_given_weights(w):
    y_predicted = lr_predictions(w, X)
    return custom_loss(y, y_predicted)
    
gradient = grad(custom_loss_given_weights)

for i in range(10000):
    if i % 1000 == 0:
        print('Iteration', i, ' | Loss:', custom_loss_given_weights(weights))
        print(weights)
    weights -= gradient(weights) * .01
    print("weight is:", weights)
    