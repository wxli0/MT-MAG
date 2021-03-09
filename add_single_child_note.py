import sys
import os 
import pandas as pd 

MLDSP_pred_path = "/Users/wanxinli/Desktop/project/BlindKameris-new/outputs/MLDSP-prediction-full-path.csv"
MLDSP_df =  pd.read_csv(MLDSP_pred_path, index_col=0, header=0, dtype = str)
print(MLDSP_df)

gtdb_tk_taxon_path = "/Users/wanxinli/Desktop/project/MLDSP-desktop/outputs/gtdbtk/gtdb-taxon.csv"
gtdb_tk_df = pd.read_csv(gtdb_tk_taxon_path, header=0, dtype = str)
gtdb_tk_df = gtdb_tk_df[['genus', 'species']]
# gtdb_tk_df = gtdb_tk_df.set_index(['genus'])
gtdb_tk_df = gtdb_tk_df.groupby('genus')['species'].apply(lambda x: sorted(list(set(x))))
gtdb_tk_df = gtdb_tk_df.to_frame()
# print(gtdb_tk_df)
for index, row in MLDSP_df.iterrows():


    # print(gtdb_tk_df.index)
    # print(index)
    # print(row)
    # print(len(row['species']))
    parent = row['genus']
    # print(parent)
    if parent not in list(gtdb_tk_df.index):
        continue

    
    children = gtdb_tk_df.loc[parent]['species']
    if 's__' in children:
        children.remove('s__')
    print(children)
    if len(children) == 1:
        print("enter this clause")
        only_child = children[0]
        MLDSP_df.at[index, 'species'] = "# only one child "+ only_child

# print(MLDSP_df)


MLDSP_df.to_csv(MLDSP_pred_path, index=True, header=True)

