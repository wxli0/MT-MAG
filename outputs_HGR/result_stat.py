import os 
import sys
import pandas as pd 
from operator import add

def correct(df, rank, index, partial=False):
    nan_count = rej_count = correct_count = partial_correct_count = wrong_count = total_count= rej_root_count = 0
    if not partial:
        pred = df.loc[index, rank]
        true = df.loc[index, rank[0].upper()+rank[1:]+ " (reference)"]
        if true == 'Unassigned':
            return [nan_count, rej_count, correct_count, partial_correct_count, wrong_count, total_count]
        total_count += 1
        if str(pred) == 'nan':
            nan_count += 1
        elif 'reject' in pred:
            rej_count += 1
        elif pred.split('__')[-1] == true:
            correct_count += 1
        else:
            wrong_count += 1
        return [nan_count, rej_count, correct_count, partial_correct_count, wrong_count, total_count]
    rank_index = all_ranks.index(rank)
    for i in reversed(range(rank_index+1)):
        cur_rank = all_ranks[i]
        cur_pred = df.loc[index, cur_rank]
        cur_true = df.loc[index, cur_rank[0].upper()+cur_rank[1:]+ " (reference)"]
        if cur_rank == rank:
            total_count += 1
        if cur_true == "Unassigned":
            continue
        if  str(cur_pred) == 'nan' or 'reject' in cur_pred:
            if cur_rank == 'phylum':
                rej_root_count += 1
            continue
        elif cur_pred.split('__')[-1] == cur_true:
            if cur_rank == rank:
                correct_count += 1
            else:
                partial_correct_count += 1
            break
        else:
            wrong_count += 1
            break
    return [nan_count, rej_count, rej_root_count, correct_count, partial_correct_count, wrong_count, total_count]
        
# e.g. python3 result_stat.py class
result_path = "HGR-prediction-full-path.csv"
results =  pd.read_csv(result_path, index_col=0, header=0, dtype = str)
# print(results)
rank = sys.argv[1]
all_ranks = ['phylum', 'class', 'order', 'family', 'genus', 'species']


total_stats = [0]*6
for index, row in results.iterrows():
    stats = correct(results, rank, index, False)
    total_stats = list( map(add, total_stats, stats) )

[nan_count, rej_count, correct_count, partial_correct_count, wrong_count, total_count] = total_stats
print("total_count:", total_count)

print("==== printing stats at", rank, "====")
print("precision:", correct_count/(total_count-rej_count-nan_count))
print("recall:", correct_count/(total_count-nan_count))
print("rejection rate:", rej_count/(total_count-nan_count))

print("==== printing stats up to", rank, "====")
print("recall:", correct_count/total_count)
print("rejection rate:", (rej_count+nan_count)/total_count)

total_stats = [0]*7
for index, row in results.iterrows():
    stats = correct(results, rank, index, True)
    total_stats = list( map(add, total_stats, stats) )
[nan_count, rej_count, rej_root_count, correct_count, partial_correct_count, wrong_count, total_count] = total_stats

print("==== if we accept partially correct prediction ====")
print("correct (including partially correct) rate:", (correct_count+partial_correct_count)/total_count)
print("incorrect rate:", wrong_count/total_count)
print("rejects at root rate", rej_root_count/total_count)