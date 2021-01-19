import os
import sys

dir = sys.argv[1]
files = os.listdir(os.path.join('/home/w328li/MLDSP/samples', dir))

for file in files:
    file = file+"_wrapper"
    os.system("python3 preprocessing.py "+file)
    print(file + "done")
