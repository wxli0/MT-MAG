import os
import sys

# e.g. python3 run_train_eval_preprocessing.py everything
dir = sys.argv[1]

os.sys("python3 preprocessing.py "+dir)
os.sys("python3 preprocessing.py "+dir+"_train")
os.sys("python3 run_preprocessing.py "+dir+"_eval")
