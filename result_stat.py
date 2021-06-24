import os
import pandas as pd


# calculates the recall
def calc_avg_recall_incorrect(path, ranks, special_pred=[]):
    df = pd.read_csv(path, header=0, index_col=0)
    recall = 0
    incorrect = 0
    for index, row in df.iterrows():
        for i in range(len(ranks)):
            cur_rank = ranks[i]
            cur_pred = str(df.loc[index][cur_rank])
            label_rank = "gtdb-tk-"+cur_rank
            label_pred = str(df.loc[index][label_rank])
            if cur_rank == ranks[-1] and cur_pred == label_pred:
                recall += 1/df.shape[0]
                break
            elif cur_rank != ranks[0]:
                pre_rank = ranks[i-1]
                pre_pred = str(df.loc[index][pre_rank])
                pre_label_rank = "gtdb-tk-"+pre_rank
                pre_label_pred = str(df.loc[index][pre_label_rank])
                if 'reject' in cur_pred and pre_pred == pre_label_pred:
                    recall += i/len(ranks)*1/df.shape[0]
                    break
            elif cur_pred in special_pred and cur_pred == label_pred:
                recall += 1/df.shape[0]
                break
            elif cur_pred != label_pred:
                incorrect += 1/df.shape[0]
                
    return recall, incorrect

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

path1 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-r202/MLDSP-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
sp1 = ['g__Prevotella']
r1, ir1 = calc_avg_recall_incorrect(path1, ranks1)
print("recall r1 is:", r1, "incorrect rate ir1:", ir1)
rej_stat1= rej_stats(path1, ranks1)
for r in rej_stat1:
    print(rej_stat1[r], "rejects at ", r)

path2 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
sp2 =  ['g__Ruminococcus_F', 'g__F0040', 'g__Pediococcus']
r2, ir2 = calc_avg_recall_incorrect(path2, ranks2, sp2)
print("recall r2 is:", r2, "incorrect rate ir1:", ir2)
rej_stat2 = rej_stats(path2, ranks2)
for r in rej_stat2:
    print(rej_stat2[r], "rejects at ", r)






            
                    



