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

total_count = 0
rej_count = 0
correct_count = 0
nan_count = 0
for pred, true in zip(res_col, comp_col):
    if true == 'Unassigned':
        continue
    total_count += 1
    if str(pred) == 'nan':
        nan_count += 1
    elif 'reject' in pred:
        rej_count += 1
    elif pred.split('__')[-1] == true:
        correct_count += 1

print("==== printing stats at", rank, "====")
print("precision:", correct_count/(total_count-rej_count-nan_count))
print("recall:", correct_count/(total_count-nan_count))
print("rejection rate:", rej_count/(total_count-nan_count))

print("==== printing stats up to", rank, "====")
print("recall:", correct_count/total_count)
print("rejection rate:", rej_count/total_count)