"""
Calcuates reliability score of a taxon based on the output of reliablity_diag_entire.py
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


bins = np.arange(0,0.01,0.001)
score_file_path = 'outputs-r202/g__UBA1232-score.txt'
score_file = open(score_file_path, 'r')
score_file_lines = score_file.readlines()
scores = []
for line in score_file_lines:
    scores.append(float(line))
ax = plt.figure().gca()
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.xticks(bins)
plt.hist(scores, bins=bins)
plt.savefig('outputs-r202'+'/'+'tmp.png')