import os

files = ["f__F082_eval_wrapper", "f__Lachnospiracea_wrapper", "f__Marinifilaceae_eval_wrapper",
    "f__Muribaculaceae_eval_wrapper", "f__Paludibacteraceae_eval_wrapper", "f__Porphyromonadaceae_eval_wrapper",
    "f__Prolixibacteraceae_eval_wrapper", "f__PUMT01_eval_wrapper", "f__Rikenellaceae_eval_wrapper",
    "f__Tannerellaceae_eval_wrapper", "f__UBA7960_eval_wrapper", "f__UBA932_eval_wrapper",
    "f__VadinHA17_eval_wrapper", "f__WCHB1-69_eval_wrapper"]

for file in files:
    os.system("python3 classify-linear-svm-ovr.py o__Bacteroidales "+file)
    print("*******", file, "done", "*******")
