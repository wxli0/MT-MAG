import os

files = ["o__Acetivibrionales_eval_wrapper",  "o__Lachnospirales_eval_wrapper",        "o__Saccharofermentanales_eval_wrapper",
        "o__Clostridiales_eval_wrapper",     "o__Oscillospirales_eval_wrapper",       "o__TANB77_eval_wrapper",
        "o__Eubacteriales_eval_wrapper",     "o__Peptostreptococcales_eval_wrapper",  "o__Tissierellales_eval_wrapper"]

for file in files:
    os.system("python3 preprocessing.py "+file)
    print(file + "done")
