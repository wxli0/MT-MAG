import pandas as pd 
import os 

# check missing predictions in HGR/MLDSP-prediction-full-path.csv
paths = ["/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-r202/MLDSP-prediction-full-path.csv", \
    "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv"]

ranks_list=  [['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species'], \
    ['phylum', 'class', 'order', 'family', 'genus', 'species']]

for path in paths:
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)
    ranks = ranks_list[paths.index(path)]

    # init missing_ranks
    missing_ranks = {}
    for r in ranks:
        missing_ranks[r] = []

    for index, row in df.iterrows():
        pre_pred = 'root'
        for r in ranks:
            cur_pred = str(df.loc[index][r])
            if 'reject' in cur_pred:
                break
            if cur_pred == 'nan':
                print(index, row)
                if pre_pred not in missing_ranks[r]:
                    missing_ranks[r].append(pre_pred)
                break
            pre_pred = cur_pred

    print(missing_ranks)


