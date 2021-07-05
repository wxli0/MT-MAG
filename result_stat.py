import os
import pandas as pd


# calculates the precision, recall, incorrect rate, partial recall
def calc_stats(path, ranks):
    df = pd.read_csv(path, header=0, index_col=0)
    partial_correct = 0
    correct = 0
    incorrect = 0
    rejected = 0
    total = 0
    for index, row in df.iterrows():
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
                
    return correct/(total-rejected), correct/total, incorrect/total, partial_correct/total



# compute rejection level statistics 
def rej_stats(path, ranks):
    # init stats
    stats = {}
    for r in ranks:
        stats[r] = 0

    df = pd.read_csv(path, header=0, index_col=0)
    for index, row in df.iterrows():
        for r in ranks:
            if 'reject' in str(df.loc[index][r]):
                stats[r] += 1
                break
    for k in stats:
        stats[k] /= df.shape[0]
    return stats

path1 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-r202-archive1/MLDSP-prediction-full-path-archive.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
precision1, recall1, incorrect_rate1, partial_recall1 = calc_stats(path1, ranks1)
print("precision is:", precision1, "recall is:", recall1, "incorrect rate is:", incorrect_rate1, "partial recall is:", partial_recall1)
# rej_stat1= rej_stats(path1, ranks1)
# for r in rej_stat1:
#     print(rej_stat1[r], "rejects at ", r)

path2 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-HGR-r202-archive1/HGR-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
precision2, recall2, incorrect_rate2, partial_recall2 = calc_stats(path2, ranks2)
print("precision is:", precision2, "recall is:", recall2, "incorrect rate is:", incorrect_rate2, "partial recall is:", partial_recall2)
# rej_stat2 = rej_stats(path2, ranks2)
# for r in rej_stat2:
#     print(rej_stat2[r], "rejects at ", r)






            
                    



