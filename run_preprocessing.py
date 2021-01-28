import os
import sys

dir = sys.argv[1]
files = os.listdir(os.path.join("data", dir))

for file in files:
    if not file.endswith('.json')
        os.system("python3 preprocessing.py "+os.path.join(dir,file))
        print(file + "done")
