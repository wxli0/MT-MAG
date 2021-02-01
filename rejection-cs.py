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
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

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

"""# Prepare model"""

import torch
from torch import nn, optim
import torch.nn.functional as F

from tqdm import trange



"""### Model"""
# max_len = 16
# x_tensor =  torch.reshape(x_tensor, [-1, max_len, 4])
# print("x_tensor_shape is:", x_tensor.shape)
# x_tensor_test =  torch.reshape(x_tensor_test, [-1, max_len, 4])

def get_mlp():
    model = nn.Sequential(
        nn.Linear(dim_features, 64),
        nn.ReLU(inplace=True),
        nn.Linear(64, num_classes),
    )
    return model


def train_model(model, optimizer, loss_func, x, y, iterations):
    for iteration in trange(iterations):
        # forward
        out = model(x)  # [batch_size, num_classes]
        loss = loss_func(out, y)
        # backward
        optimizer.zero_grad()
        loss.backward()
        # clip gradients
        clipping_value = 1 
        torch.nn.utils.clip_grad_norm(model.parameters(), clipping_value)
        print("***** iteration:", iteration, "******")
        # print("print gradients:")
        # for p in model.parameters():
        #     if p.grad is not None:
        #         print(p.grad.data)
        optimizer.step()
        print("loss:", loss.item())



"""---

# Cost-sensitive approach: https://arxiv.org/abs/2010.11748
"""

def cost_sensitive_loss(loss_func, rej_cost):
    def loss(out, y):
        batch_size, num_classes = out.shape
        mask = torch.eye(num_classes, num_classes).long()
        
        out_p = out.masked_select(mask[y] == 1)  # [batch_size]
        out_n = out.masked_select(mask[y] == 0)  # [batch_size * (num_classes - 1)]
        
        l_p = loss_func(out_p)  # [batch_size]
        l_n = loss_func(-out_n)  # [batch_size * (num_classes - 1)]
        
        # sum -> weighted average -> batch average
        return (rej_cost * l_p.sum() + (1 - rej_cost) * l_n.sum()) / batch_size
        
    return loss

"""# Prepare data"""
def update_y_test_values(y_test, dict):
    # transform y to values in label_dict
    trans_dict = {}
    if train_folder.startswith('c'):
        trans_dict = json.load(open('label_dict/class_dict.json'))
    elif train_folder.startswith('d'):
        trans_dict = json.load(open('label_dict/domain_dict.json'))
    if train_folder.startswith('o'):
        trans_dict = json.load(open('label_dict/order_dict.json'))
    if train_folder.startswith('p'):
        trans_dict = json.load(open('label_dict/phylum_dict.json'))
    y_test_new = []
    for i in range(len(y_test)):
        i_short = y_test[i]
        if i_short.endswith('_test'):
            i_short = i_short[:-5]
        y_test_new.append(trans_dict[i_short])
    return update_y_values(y_test_new, dict)

train, tests = read_pfiles_more_test(sys.argv[1])
test_folders = json.load(open(sys.argv[1]))['test_folders']
train_folder = json.load(open(sys.argv[1]))['train_folder']


k = 7
x, y = p_files_to_normal(train, k)
print("x shape is:", x.shape)
print("y shape is:", y.shape)

y_dict = {}
y_unique = np.unique(y)
for i in range(len(y_unique)):
    y_dict[y_unique[i]] = i
    y_dict[y_unique[i]+'_eval'] = i
    y_dict[y_unique[i]+'_test'] = i
print("y_dict is:", y_dict)

y = update_y_values(y, y_dict)



scaler = StandardScaler(with_mean=False)
svd = TruncatedSVD(n_components=5, n_iter=7, random_state=42)
x = scaler.fit_transform(x)
x = svd.fit_transform(x)



num_classes = len(np.unique(y))
dim_features = x.shape[1]
print("x.shape is:", x.shape, "y.len is:", len(y))

x_tensor = torch.tensor(x).float()
y_tensor = torch.tensor(y).long()

"""## Train """

# setup
model_cost = get_mlp()
optimizer = optim.AdamW(model_cost.parameters())
loss_func = cost_sensitive_loss(losses[loss_name_cost], rej_cost=rej_cost)

# training
train_model(model_cost, optimizer, loss_func, x_tensor, y_tensor, 3000)

"""## Test"""

def cs_reject(t):
    top1, top2 = t.topk(2, dim=1)[0].T
    return (top1 < 0) | (top2 > 0)

for i in range(len(tests)):
    test = tests[i]
    print("======== testing", test_folders[i], "=========")
    x_test, y_test = p_files_to_normal(test, k)
    y_test = update_y_test_values(y_test, y_dict)
    x_test = scaler.transform(x_test)
    x_test = svd.transform(x_test)
    print("x_test.shape is:", x_test.shape, "y_test.len is:", len(y_test))

    """### Convert data to tensor"""

    x_tensor_test = torch.tensor(x_test).float()
    y_tensor_test = torch.tensor(y_test).long()

    out_test = model_cost(x_tensor_test)
    print("out_test is:")
    print(out_test)
    rejected = cs_reject(out_test)
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
    if num_selected == 0:
        print("Accuracy of non-rejected data: NA" )
    else:
        print(f"Accuracy of non-rejected data: {num_correct / num_selected * 100:.2f} % ({num_correct}/{num_selected})")
    print(f"Test empirical 0-1-c risk: {zero_one_c:.6f}")

