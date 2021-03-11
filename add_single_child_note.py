import sys
import os 
import pandas as pd 

# 
rank = sys.argv[1]
next_rank = sys.argv[2]
MLDSP_pred_path = "/Users/wanxinli/Desktop/project/BlindKameris-new/outputs/MLDSP-prediction-full-path.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
print(MLDSP_df)

gtdb_tk_taxon_path = "/Users/wanxinli/Desktop/project/MLDSP-desktop/outputs/gtdbtk/gtdb-taxon.csv"
gtdb_tk_df = pd.read_csv(gtdb_tk_taxon_path, header=0, dtype = str)
gtdb_tk_df = gtdb_tk_df[[rank, next_rank]]
# gtdb_tk_df = gtdb_tk_df.set_index(['genus'])
gtdb_tk_df = gtdb_tk_df.groupby(rank)[next_rank].apply(lambda x: sorted(list(set(x))))
gtdb_tk_df = gtdb_tk_df.to_frame()
# print(gtdb_tk_df)

for index, row in MLDSP_df.iterrows():
    parent = row[rank]
    # print(parent)
    if parent not in list(gtdb_tk_df.index):
        continue

    
    children = gtdb_tk_df.loc[parent][next_rank]
    if next_rank[:1]+"__" in children:
        children.remove(next_rank[:1]+"__")
    print(children)
    if len(children) == 1:
        print("enter this clause")
        only_child = children[0]
        MLDSP_df.at[index, next_rank] = "# only one child "+ only_child

# print(MLDSP_df)


MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)

