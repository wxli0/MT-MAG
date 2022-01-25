import openpyxl
import os
import pandas as pd 


def find_single_child(path, ranks, dir, suffix = ""):
    """
    Find exiting single child taxons in a classification result file
    
    :param path: path of the classification result file
    :type path: str
    :param ranks: list of ranks in the classification result file
    :type ranks: List(str)
    :param dir: directory of training dataset
    :type dir: str
    :param suffix: suffix of the subdirectories in the dir
    :type suffix: str
    """
    single_child_taxons = []
    df = pd.read_csv(path, index_col=0, header=0, dtype = str)
    all_taxons = []
    for rank in ranks:
        all_taxons.extend(list(df[rank]))
    all_taxons = list(set(all_taxons))
    for taxon in all_taxons:
        taxon = str(taxon)
        if 'uncertain' in taxon or taxon == 'nan':
            continue
        children = os.listdir(os.path.join(dir,taxon+suffix))
        if len(children) == 1:
            single_child_taxons.append(taxon)
    return single_child_taxons

def update_single_child(single_child, output_dir):
    for child in single_child:
        file = os.path.join(output_dir, child+".xlsx")
        sheet = child+"_pred-t-p"
        df = pd.read_excel(file, index_col=0, header=0, sheet_name=sheet)
        rejection_f = []
        for index, row in df.iterrows():
            if float(row['max']) < 0:
                rejection_f.append(row['prediction']+'(uncertain)')
            else:
                rejection_f.append(row['prediction'])
        if 'rejection-f' in df.columns:
            del df['rejection-f']
        df['rejection-f'] = rejection_f

        wb = openpyxl.load_workbook(file)
        del wb[sheet]

        mode = 'w'
        if len(wb.sheetnames) != 0:
            wb.save(file)
            mode = 'a'

        with pd.ExcelWriter(file, engine="openpyxl", mode=mode) as writer:  
            df.to_excel(writer, sheet_name = sheet, index=True)
            writer.save()


print("HGR")
HGR_single_child = find_single_child('~/MT-MAG/outputs-HGR-r202-archive3/HGR-r202-prediction-full-path.csv', \
    ['phylum', 'class', 'order', 'family', 'genus'], '/mnt/sda/DeepMicrobes-data/labeled_genome-r202')
print("HGR single child are:", HGR_single_child)
# HGR_single_child = ['g__RUG678', 'g__RUG147', 'g__RUG013', 'g__UBA9722', 'f__RUG033', 'c__Methanobacteria', 'c__Clostridia_A', 'g__RUG714', 'f__UBA1188', 'c__Ozemobacteria', 'g__RUG334', 'o__Ozemobacterales', 'g__RUG100', 'f__UBA3663', 'p__RUG730', 'o__RF39', 'g__Kandleria', 'g__RUG708', 'g__UBA2942', 'f__RUG350', 'g__CADAUA01', 'c__Desulfovibrionia', 'p__Riflebacteria']
# update_single_child(HGR_single_child, './outputs-HGR-r202-archive3')


print("GTDB")
GTDB_single_child = find_single_child('~/MT-MAG/outputs-GTDB-r202-archive3/GTDB-r202-prediction-full-path.csv', \
    ['domain', 'phylum', 'class', 'order', 'family', 'genus'], '/mnt/sda/MLDSP-samples-r202')
print("GTDB single child are:", GTDB_single_child)
# GTDB_single_child = ['g__RUG678', 'g__RUG147', 'g__RUG013', 'g__UBA9722', 'f__RUG033', 'c__Methanobacteria', 'c__Clostridia_A', 'g__RUG714', 'f__UBA1188', 'c__Ozemobacteria', 'g__RUG334', 'o__Ozemobacterales', 'g__RUG100', 'f__UBA3663', 'p__RUG730', 'o__RF39', 'g__Kandleria', 'g__RUG708', 'g__UBA2942', 'f__RUG350', 'g__CADAUA01', 'c__Desulfovibrionia', 'p__Riflebacteria']
# update_single_child(GTDB_single_child, './outputs-GTDB-r202-archive3')



