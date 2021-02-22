import os
import sys

# e.g. python3 run_train_eval_preprocessing.py everything
dir = sys.argv[1]
files = os.listdir(os.path.join("data", dir))

os.sys("python3 preprocessing.py "+os.path.join(dir))
os.sys("python3 preprocessing.py "+os.path.join(dir+"_train"))
os.sys("python3 run_preprocessing.py "+os.path.join(dir))
