import os
import pandas as pd


# calculates the recall
def calc_partial_recall_incorrect(path, ranks, special_pred=[]):
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

def calc_recall(path, ranks, special_pred=[]):
    df = pd.read_csv(path, header=0, index_col=0)
    rejected = 0
    correct = 0
    total = 0
    for index, row in df.iterrows():
        cur_rank = ranks[-1]
        cur_pred = str(df.loc[index][cur_rank])
        label_rank = "gtdb-tk-"+cur_rank
        label_pred = str(df.loc[index][label_rank])
        if str(cur_pred) != 'nan' and df.loc[index]['gtdb-tk-species'] != 's__' and df.loc[index]['gtdb-tk-genus'] != 'g__':
            total += 1
            if cur_pred == label_pred:
                correct += 1
    return correct/total


path1 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-r202/MLDSP-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
r1 = calc_recall(path1, ranks1)
print("recall r1 is:", r1)

path2 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
r2 = calc_recall(path2, ranks2)
print("recall r1 is:", r2)






            
                    



