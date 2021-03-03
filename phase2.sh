#!/bin/bash

output1="outputs/$1.xlsx"
rej="rejection_threshold/$1.json"
python3 preprocess_test.py ${output1} ${rej}

python3 add_MLDSP_pred.py ${output1}