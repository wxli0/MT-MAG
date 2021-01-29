import sys
import pandas as pd
import openpyxl

file_name = sys.argv[1]
sheet_name = sys.argv[2]
taxon = sys.argv[3]

# e.g.  python3 add_true_prediction.py outputs/glv_test.xlsx d__Bacteria_p__Firmicutes_A-t-p phylum 

df = pd.read_excel(file_name, index_col=0, header=0, sheet_name=sheet_name)
true_df = pd.read_csv('outputs/glv_mags_qual_tax_summary.tsv', sep='\t', index_col=0, header=0)

if 'GTDB-Tk prediction' not in df.columns:
    true_pred = []
    for index, row in df.iterrows():
        true_pred.append(true_df.loc[index][taxon])

    df['GTDB-Tk prediction'] = true_pred

    workbook=openpyxl.load_workbook(file_name)
    std=workbook.get_sheet_by_name(sheet_name)
    workbook.remove(std)
    workbook.save(file_name)

    with pd.ExcelWriter(file_name, engine="openpyxl", mode='a') as writer:  
        df.to_excel(writer, sheet_name =sheet_name, index=True)
    writer.save()
    writer.close()
