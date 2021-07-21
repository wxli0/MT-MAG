import os
import pandas as pd


# calculates the precision, recall, incorrect rate, partial recall, rejection rate at different levels
def calc_stats(path, ranks, ignore_taxons =[]):
    df = pd.read_csv(path, header=0, index_col=0)
    partial_correct = 0
    correct = 0
    incorrect = 0
    rejected = 0
    total = 0
    # init rej_stats
    rej_stats = {}
    for r in ranks:
        rej_stats[r] = 0

    for index, row in df.iterrows():
        if df.loc[index]['gtdb-tk-species'] == 's__':
            continue
        if df.loc[index]['genus'] in ignore_taxons:
            continue
        for i in range(len(ranks)):
            cur_rank = ranks[i]
            cur_pred = str(df.loc[index][cur_rank])
            label_rank = "gtdb-tk-"+cur_rank
            label_pred = str(df.loc[index][label_rank])
            pre_rank = ranks[i-1]
            pre_pred = str(df.loc[index][pre_rank])
            pre_label_rank = "gtdb-tk-"+pre_rank
            pre_label_pred = str(df.loc[index][pre_label_rank])
            if cur_rank == ranks[-1] and cur_pred == label_pred:
                partial_correct += 1
                correct += 1
                total += 1
                break
            elif (cur_rank != ranks[0] and 'reject' in cur_pred and pre_pred == pre_label_pred) \
                or cur_rank == ranks[0] and 'reject' in cur_pred:
                partial_correct += i/len(ranks)
                total += 1
                rejected += 1
                break
            elif cur_pred != label_pred and cur_pred != 'nan':
                incorrect += 1
                total += 1
                break

    for index, row in df.iterrows():
        for r in ranks:
            if 'reject' in str(df.loc[index][r]):
                rej_stats[r] += 1
                break
            
    for k in rej_stats:
        rej_stats[k] /= total
                
    return correct/(total-rejected), correct/total, incorrect/total, partial_correct/total, rej_stats




path1 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-r202/MLDSP-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
precision1, recall1, incorrect_rate1, partial_recall1, rej_stats1 = calc_stats(path1, ranks1)
print("precision is:", precision1, "recall is:", recall1, "incorrect rate is:", incorrect_rate1, "partial recall is:", partial_recall1)
for r in rej_stats1:
    print(rej_stats1[r], "rejects at ", r)
print("total rejection rate is:", sum(rej_stats1.values()))

path2 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_taxons2 = ['g__Pediococcus', 'g__Ruminococcus_F', 'g__F0040']
precision2, recall2, incorrect_rate2, partial_recall2, rej_stats2 = calc_stats(path2, ranks2)
print("precision is:", precision2, "recall is:", recall2, "incorrect rate is:", incorrect_rate2, "partial recall is:", partial_recall2)
for r in rej_stats2:
    print(rej_stats2[r], "rejects at ", r)
print("total rejection rate is:", sum(rej_stats2.values()))





            
                    



