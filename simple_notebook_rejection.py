# -*- coding: utf-8 -*-
"""simple_notebook_rejection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vplDAuD_PwIY9uM2gNSLKCZ3ELlxfiBi

# Written by Nontawat Charoenphakdee and Yivan Zhang.
"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors
import math
import sys
from classifyhelpers import *

np.random.seed(2020)

"""# Losses"""

sigmoid = lambda z: torch.sigmoid(-z)
ramp = lambda z: torch.clamp((1 - z) / 2, min=0, max=1)
logistic = lambda z: torch.log(1 + torch.exp(-z))
exponential = lambda z: torch.exp(-z)
hinge = lambda z: torch.clamp(1 - z, min=0)
squared = lambda z: (1 - z).pow(2)
unhinged = lambda z: 1 - z
savage = lambda z: torch.sigmoid(-2 * z).pow(2)
tangent = lambda z: (2 * torch.atan(z) - 1).pow(2)
almost = lambda z: torch.sigmoid(-2 * z).pow(1.5)

# classification-calibrated losses
losses = {
    # proper composite losses -> applicable to both confidence-based and cost-senstive approach
    "logistic": lambda z: torch.log(1 + torch.exp(-z)),
    "exp": lambda z: torch.exp(-z),
    "square": lambda z: (1 - z).pow(2),
    "savage": lambda z: torch.sigmoid(-2 * z).pow(2),
    "tangent": lambda z: (2 * torch.atan(z) - 1).pow(2),
    # non-proper composite losses -> not applicable to the confidence-based approach but applicable to the cost-sensitive approach  
    "sigmoid": lambda z: torch.sigmoid(-z),
    "hinge": lambda z: torch.clamp(1 - z, min=0),
    "unhinge": lambda z: 1 - z,
    "ramp": lambda z: torch.clamp((1 - z) / 2, min=0, max=1),
}

# link function is only available for proper composite losses
links = {
    "logistic": lambda p: math.log(p / (1 - p)),
    "exp": lambda p: 0.5 * math.log(p / (1 - p)),
    "square": lambda p: 2 * p - 1,
    "savage": lambda p: math.log(p / (1 - p)),
    "tangent": lambda p: math.tan(p - 0.5),
}

"""# Arguments"""

# loss for the one-vs-all (ova) approach
loss_name_ova = 'logistic'
# loss for the cost-sensitive approach
loss_name_cost = 'hinge'
rej_cost = 0.25

"""# Prepare data"""
train_folder = sys.argv[1]
test_folder = sys.argv[2]

dest_folder = "p_files/"

train_filename = dest_folder+train_folder+'.p'
test_filename = dest_folder+test_folder+'.p'

train, test = read_pfiles(train_filename, test_filename)

k = 7
x, y = p_files_to_normal(train, k)
print("x shape is:", x.shape)
print("y shape is:", y.shape)

y_dict = {}
y_unique = np.unique(y)
for i in range(len(y_unique)):
    y_dict[y_unique[i]] = i
    y_dict[y_unique[i]+'_eval'] = i
print("y_dict is:", y_dict)

y = update_y_values(y, y_dict)

x_test, y_test = p_files_to_normal(test, k)
y_test = update_y_values(y_test, y_dict)


num_classes = len(np.unique(y))
dim_features = x.shape[1]



"""# Prepare model"""

import torch
from torch import nn, optim
import torch.nn.functional as F

from tqdm import trange

"""### Convert data to tensor"""

x_tensor = torch.tensor(x).float()
print("y is", y)

y_tensor = torch.tensor(y).long()
x_tensor_test = torch.tensor(x_test).float()
y_tensor_test = torch.tensor(y_test).long()

"""### Model"""

def get_mlp():
    model = nn.Sequential(
        nn.Linear(dim_features, 64),
        nn.ReLU(inplace=True),
        nn.Linear(64, num_classes),
        nn.Softmax()
    )
    return model

def train(model, optimizer, loss_func, x, y, iterations):
    for iteration in trange(iterations):
        # forward
        out = model(x)  # [batch_size, num_classes]
        loss = loss_func(out, y)
        # backward
        optimizer.zero_grad()
        loss.backward()
        # # clip gradients
        # clipping_value = 1 
        # torch.nn.utils.clip_grad_norm(model.parameters(), clipping_value)
        print("***** iteration:", iteration, "******")
        print("print gradients:")
        for p in model.parameters():
            if p.grad is not None:
                print(p.grad.data)
        optimizer.step()
        print("loss:", loss.item())

"""---

# One-vs-all loss (confidence-based approach): https://arxiv.org/abs/1901.10655
"""

def one_vs_all_loss(loss_func):
    def loss(out, y):
        batch_size, num_classes = out.shape
        mask = torch.eye(num_classes, num_classes).long()
        
        out_p = out.masked_select(mask[y] == 1)  # [batch_size]
        out_n = out.masked_select(mask[y] == 0)  # [batch_size * (num_classes - 1)]
        
        l_p = loss_func(out_p)  # [batch_size]
        print("out_p is:", out_p)
        print("l_p is:", l_p)

        l_n = loss_func(-out_n)  # [batch_size * (num_classes - 1)]
        print("-out_n is:", -out_n)
        print("l_n is:", l_n)
        
        # sum -> batch average
        return (l_p.sum() + l_n.sum()) / batch_size
        
    return loss

"""## Train"""

# setup
model_ova = get_mlp()
optimizer = optim.AdamW(model_ova.parameters())
loss_func = one_vs_all_loss(losses[loss_name_ova])

# training
print("start training")
train(model_ova, optimizer, loss_func, x_tensor, y_tensor, 1000)

"""## Test"""

def conf_reject(threshold: float):
    def reject(t):
        return t.max(dim=1)[0] < threshold

    return reject

print("start testing")
out_test = model_ova(x_tensor_test)
print("predicted is:", out_test)
rejected = conf_reject(-links[loss_name_ova](rej_cost))(out_test)
result = torch.zeros_like(y_tensor_test)
result[rejected] = -1
result[~rejected & (y_tensor_test == out_test.argmax(1))] = 1

num_data = len(result)
num_rejected = (result == -1).sum().item()
num_wrong = (result == 0).sum().item()
num_correct = (result == 1).sum().item()
num_selected = num_wrong + num_correct
zero_one_c = (num_wrong + rej_cost * num_rejected) / num_data

print(f"Number of rejected data: {num_rejected / num_data * 100:.2f}% ({num_rejected}/{num_data})")
print(f"Accuracy of non-rejected data: {num_correct / num_selected * 100:.2f} % ({num_correct}/{num_selected})")
print(f"Test empirical 0-1-c risk: {zero_one_c:.6f}")
