import os 
import sys
import pandas as pd 
from operator import add
import matplotlib.pyplot as plt

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
        return [nan_count, rej_count, correct_count, wrong_count, total_count]
    rank_index = all_ranks.index(rank)
    partial_correct_list = [0]*len(all_ranks)

    cur_rank_true = df.loc[index, rank[0].upper()+ rank[1:]+ " (reference)"]
    for i in reversed(range(rank_index+1)):
        cur_rank = all_ranks[i]
        cur_pred = df.loc[index, cur_rank]
        cur_true = df.loc[index, cur_rank[0].upper()+cur_rank[1:]+ " (reference)"]
        if cur_rank == rank and cur_true == "Unassigned":
            break
        if cur_rank_true not in genus_dict:
            genus_dict[cur_rank_true] = [0]*3
        if cur_rank == rank:
            total_count += 1
            genus_dict[cur_rank_true][2] += 1
        if cur_true == "Unassigned":
            continue
        if  str(cur_pred) == 'nan' or 'reject' in cur_pred:
            if cur_rank == 'phylum':
                rej_root_count += 1
            continue
        elif cur_pred.split('__')[-1] == cur_true:
            if cur_rank == rank:
                correct_count += 1
                genus_dict[cur_rank_true][0] += 1
            else:
                partial_correct_count += 1
                partial_correct_list[i] += 1
                genus_dict[cur_rank_true][1] += 1
            break
        else:
            wrong_count += 1
            break
    return [nan_count, rej_count, rej_root_count, correct_count, \
        partial_correct_count, wrong_count, total_count], partial_correct_list
        
# e.g. python3 result_stat.py class
result_path = "HGR-prediction-full-path-old.csv"
results =  pd.read_csv(result_path, index_col=0, header=0, dtype = str)
# print(results)
rank = sys.argv[1]
all_ranks = ['phylum', 'class', 'order', 'family', 'genus', 'species']


total_stats = [0]*5
for index, row in results.iterrows():
    stats = correct(results, rank, index, False)
    total_stats = list( map(add, total_stats, stats) )

[nan_count, rej_count, correct_count, wrong_count, total_count] = total_stats
print("total_count:", total_count)

print("==== if we do not accept partially correct prediction ====")
print("==== printing stats at", rank, "====")
print("precision:", correct_count/(total_count-rej_count-nan_count))
print("recall:", correct_count/(total_count-nan_count))
print("rejection rate:", rej_count/(total_count-nan_count))

print("==== printing stats up to", rank, "====")
print("recall:", correct_count/total_count)
print("rejection rate:", (rej_count+nan_count)/total_count)

genus_dict = {}

total_stats = [0]*7
partial_correct_list = [0]*len(all_ranks)
for index, row in results.iterrows():
    stats, cur_partial_correct_list = correct(results, rank, index, True)
    total_stats = list( map(add, total_stats, stats) )
    partial_correct_list = list(map(add, partial_correct_list, cur_partial_correct_list))
[nan_count, rej_count, rej_root_count, correct_count, partial_correct_count, wrong_count, total_count] = total_stats

print("==== if we accept partially correct prediction ====")
print("correct rate:", correct_count/total_count)
print("partially correct rate:", partial_correct_count/total_count)
for i in range(len(all_ranks)-2): # -2 as we stop at genus classification
    print("partially correct and rejects at "+all_ranks[i+1]+" rate:", partial_correct_list[i]/sum(partial_correct_list))
print("incorrect rate:", wrong_count/total_count)
print("rejects at phylum rate", rej_root_count/total_count)

print(genus_dict)

langs = []
incorrect_rates = []
widths = []
for key, value in genus_dict.items():
    langs.append(key)
    incorrect_rates.append((value[2]-value[0]-value[1])/value[2])
    widths.append(value[2])

fig = plt.figure()
widths = [20*w/sum(widths) for w in widths]
plt.bar(langs,incorrect_rates, width=widths)
plt.suptitle('Incorrect rates vs checkM genus labels')
plt.xticks(rotation='82.5', fontsize=2.8)
plt.xlabel('checkM genus labels')
plt.ylabel('incorrect rate')
plt.savefig('incorrect_rate_by_genus_labels.png',dpi=400)
# plt.show()
