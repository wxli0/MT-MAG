import numpy as np
import pandas as pd

def clean_result(path, ranks):
    df = pd.read_csv(path, header=0, index_col=0)
    incomplete = []
    for index, row in df.iterrows():
        valid = np.nan
        for i in range(len(ranks)):
            r = ranks[i]
            cur_pred = df.loc[index][r]
            if str(cur_pred) != 'nan':
                valid = cur_pred
            if 'uncertain' in str(cur_pred) or 'reject' in str(cur_pred):
                for j in range(i+1, len(ranks)):
                    r = ranks[j]
                    df.at[index, r] = np.nan
                break
            if r == ranks[-1] and str(cur_pred) == 'nan':
                print(index)
                if valid not in incomplete:
                    incomplete.append(valid)
    return df, incomplete

path1 = "./outputs-GTDB-r202/GTDB-r202-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']

df1, incomplete1 = clean_result(path1, ranks1)
print("incomplete1 is:", incomplete1)
df1.to_csv(path1)

path2 = "./outputs-HGR-r202/HGR-r202-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
df2, incomplete2 = clean_result(path2, ranks2)
print("incomplete2 is:", incomplete2)
df2.to_csv(path2)