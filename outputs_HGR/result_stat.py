import os 
import sys
import pandas as pd 

# e.g. python3 result_stat.py class
result_path = "HGR-prediction-full-path.csv"
results =  pd.read_csv(result_path, index_col=0, header=0, dtype = str)
# print(results)
rank = sys.argv[1]
res_col = results[rank]
# print(res_col)

comp_rank = rank[0].upper()+rank[1:]+ " (reference)"
# print(comp_rank)
comp_col = results[comp_rank]
# print(comp_col)

total = 0
rej_count = 0
correct_count = 0
stop_count = 0
for pred, true in zip(res_col, comp_col):
    # print(pred, true)
    if str(pred) == 'nan' or true == 'Unassigned':
        continue
    total += 1
    if 'reject' in pred:
        rej_count += 1
    elif 'stop' in pred:
        stop_count += 1
    elif pred.split('__')[-1] == true:
        correct_count += 1

print("==== printing stats for", rank, " ====")
print("precision:", correct_count/(total-rej_count-stop_count))
print("recall:", correct_count/total)
print("rejection rate:", rej_count/total)
print("stop rate:", stop_count/total)