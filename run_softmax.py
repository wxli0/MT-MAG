import os

files = ["f__F082_eval-LSVM", "f__Lachnospiracea-LSVM", "f__Marinifilaceae_eval-LSVM",
    "f__Muribaculaceae_eval-LSVM", "f__Paludibacteraceae_eval-LSVM", "f__Porphyromonadaceae_eval-LSVM",
    "f__Prolixibacteraceae_eval-LSVM", "f__PUMT01_eval-LSVM", "f__Rikenellaceae_eval-LSVM",
    "f__Tannerellaceae_eval-LSVM", "f__UBA7960_eval-LSVM", "f__UBA932_eval-LSVM",
    "f__VadinHA17_eval-LSVM", "f__WCHB1-69_eval-LSVM"]

for file in files:
    os.system("python3 add_softmax.py outputs/fft-o__Bacteroidales.xlsx "+file)
    print(file + " done")
