"""
Calculates the precision, recall, incorrect rate, partial recall, \
    rejection rate at different levels for MT-MAG classificaton result \
        in HGR/GTDB-prediction-full-path.csv.

No command line arguments are required.
"""

import pandas as pd
import statistics as stat


def calc_stats(path, path_true, ranks, ignore_taxa =[], ignore_indices = []):
    """
    Calculates the precision, recall, incorrect rate, partial recall, \
        rejection rate at different levels for MT-MAG classificaton result.
    
    Not in use.

    :param path: path of the classification result file.
    :type path: str
    :param ranks: ranks in the classification result file.
    :type ranks: List[str]
    :param ignore_taxa: taxa to ignore in the calculation
    :type ignore_taxa: List[str]
    :param ignore_indices: test indices to ignore in the calculation
    :type ignore_indices: List[str]
    """
    df = pd.read_csv(path, header=0, index_col=0)
    df_true = pd.read_csv(path_true, header=0, index_col=0)
    partial_correct = 0
    correct = 0
    incorrect = 0
    rejected = 0
    total = 0
    # init rej_stats
    rej_stats = {}
    for r in ranks:
        rej_stats[r] = 0

    partial_correct = 0
    for index, row in df.iterrows():
        if index in ignore_indices:
            continue
        row_true = df_true.loc[index]
        true_label = str(row_true['gtdb-tk-'+ranks[-1]])
        if true_label== 's__':
            continue
        if row['genus'] in ignore_taxa \
            or row['family'] in ignore_taxa:
            continue
        predicted_label  = str(row[ranks[-1]])
        # 'reject' is in prediction
        if 'uncertain' in predicted_label or predicted_label == 'nan':
            rejected += 1
            correct_rank = 0
            # find the rejected label
            for rank in ranks:
                pred_rank = 'gtdb-tk-'+rank
                true_rank_label = str(row_true[pred_rank])
                pred_rank_label = str(row[rank])
                # print("true_rank_label is:", true_rank_label)
                # print("pred_rank_label is:", pred_rank_label)
                if 'uncertain' in pred_rank_label:
                    break
                elif true_rank_label == pred_rank_label:
                    correct_rank += 1
                else:
                    correct_rank = 0
            # print("correct_rank is:", correct_rank)
            partial_correct += correct_rank


        elif predicted_label == true_label:
            correct += 1
            partial_correct += len(ranks)
        else:
            incorrect += 1

    for index, row in df.iterrows():
        for r in ranks:
            if 'uncertain' in str(df.loc[index][r]):
                rej_stats[r] += 1
                break

    total = correct+incorrect+rejected    
    for i in range(1, len(ranks)):
        rank = ranks[i]
        pre_rank = ranks[i-1]
        rej_stats[rank] += rej_stats[pre_rank]

    for k in rej_stats:
        rej_stats[k] /= total
    classified_acc = correct/(correct+incorrect)
    absolute_acc = correct/total
    adjusted_acc = (correct+0.5*rejected)/total
    partial_acc = partial_correct/((correct+incorrect+rejected)*len(ranks))
    return classified_acc, absolute_acc, adjusted_acc, partial_acc, rej_stats


def calc_stats_per_rank(path, path_true, ranks, ignore_taxa =[], ignore_indices = []):
    """
    Calculates the constrained accuracy, absolate accuracy, weighted accuracy, \
        partial rate at rank for MT-MAG classificaton result.
    

    :param path: path of the classification result file.
    :type path: str
    :param ranks: ranks in the classification result file.
    :type ranks: List[str]
    :param ignore_taxa: taxa to ignore in the calculation
    :type ignore_taxa: List[str]
    :param ignore_indices: test indices to ignore in the calculation
    :type ignore_indices: List[str]
    """
    df = pd.read_csv(path, header=0, index_col=0)
    df_true = pd.read_csv(path_true, header=0, index_col=0)
    CAs = []
    AAs = []
    WAs = []
    PRs = []
    
    for rank in ranks:
        correct = 0
        rejected = 0
        total = 0
        for index, row in df.iterrows():
            # skip cases
            if index in ignore_indices:
                continue
            row_true = df_true.loc[index]
            species_label = str(row_true['gtdb-tk-'+ranks[-1]])
            if species_label== 's__':
                continue
            if row[rank] in ignore_taxa:
                ignore_indices.append(index)
                continue

            # count cases
            total += 1
            predicted_label  = str(row[rank])
            true_label = str(row_true['gtdb-tk-'+rank])
            if true_label == predicted_label:
                correct += 1
            elif 'uncertain' in predicted_label or 'reject' in predicted_label or predicted_label == 'nan':
                rejected += 1
        CA = correct/(total-rejected)
        AA = correct/total
        WA = (correct+0.5*rejected)/total
        PR = rejected/total
        CAs.append(CA)
        AAs.append(AA)
        WAs.append(WA)
        PRs.append(PR)
        print("at", rank, "CA:", "{:.2%}".format(CA), "AA:", "{:.2%}".format(AA), \
            "WA:", "{:.2%}".format(WA), "PCR:", "{:.2%}".format(PR), "1-PCR:", "{:.2%}".format(1-PR))
    print("avg CA:", "{:.2%}".format(stat.mean(CAs)), "avg AA:", "{:.2%}".format(stat.mean(AAs)), \
        "avg WA:", "{:.2%}".format(stat.mean(WAs)), "avg PCR:", "{:.2%}".format(stat.mean(PRs)))







print("====== HGR result ======")

path_true2 = "./outputs-HGR-r202-archive1/HGR-r202-prediction-full-path.csv"
path2 = "outputs-HGR-r202-archive3/HGR-r202-archive3-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_indices2 = ['MAG-GUT10417.fa', 'MAG-GUT15880.fa', 'MAG-GUT1743.fa', 'MAG-GUT21953.fa', 'MAG-GUT22878.fa', 'MAG-GUT28136.fa', 'MAG-GUT29051.fa', 'MAG-GUT29076.fa', 'MAG-GUT33914.fa', 'MAG-GUT36027.fa', 'MAG-GUT40857.fa', 'MAG-GUT41924.fa', 'MAG-GUT42485.fa', 'MAG-GUT42494.fa', 'MAG-GUT42584.fa', 'MAG-GUT43216.fa', 'MAG-GUT43894.fa', 'MAG-GUT44111.fa', 'MAG-GUT44851.fa', 'MAG-GUT45331.fa', 'MAG-GUT46923.fa', 'MAG-GUT47106.fa', 'MAG-GUT47179.fa', 'MAG-GUT4902.fa', 'MAG-GUT52094.fa', 'MAG-GUT52107.fa', 'MAG-GUT52138.fa', 'MAG-GUT53617.fa', 'MAG-GUT54931.fa', 'MAG-GUT56425.fa', 'MAG-GUT5727.fa', 'MAG-GUT58014.fa', 'MAG-GUT58077.fa', 'MAG-GUT59039.fa', 'MAG-GUT60365.fa', 'MAG-GUT61159.fa', 'MAG-GUT61176.fa', 'MAG-GUT61959.fa', 'MAG-GUT70200.fa', 'MAG-GUT7064.fa', 'MAG-GUT7066.fa', 'MAG-GUT7291.fa', 'MAG-GUT76426.fa', 'MAG-GUT77982.fa', 'MAG-GUT78879.fa', 'MAG-GUT78908.fa', 'MAG-GUT78923.fa', 'MAG-GUT81671.fa', 'MAG-GUT82176.fa', 'MAG-GUT82203.fa', 'MAG-GUT83501.fa', 'MAG-GUT83507.fa', 'MAG-GUT83946.fa', 'MAG-GUT8428.fa', 'MAG-GUT84696.fa', 'MAG-GUT84793.fa', 'MAG-GUT8521.fa', 'MAG-GUT86514.fa', 'MAG-GUT86868.fa', 'MAG-GUT87091.fa', 'MAG-GUT87486.fa', 'MAG-GUT87573.fa', 'MAG-GUT87828.fa', 'MAG-GUT88085.fa', 'MAG-GUT88218.fa', 'MAG-GUT88257.fa', 'MAG-GUT88679.fa', 'MAG-GUT88862.fa', 'MAG-GUT89291.fa', 'MAG-GUT89323.fa', 'MAG-GUT90190.fa', 'MAG-GUT90947.fa', 'MAG-GUT91328.fa']
# ignore_taxa2 = ['o__Lachnospirales', 'f__Ruminococcaceae', 'f__Oscillospiraceae', 'g__Prevotella']
calc_stats_per_rank(path2, path_true2, ranks2, ignore_indices=ignore_indices2, ignore_taxa=[])


print("====== GTDB result ======")
true_path1 = "./outputs-GTDB-r202-archive1/GTDB-r202-prediction-full-path.csv"
path1 = "outputs-GTDB-r202-archive3/GTDB-r202-archive3-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_indices1 =  ['RUG428.fasta', 'RUG635.fasta', 'RUG684.fasta', 'RUG687.fasta', 'RUG732.fasta', 'RUG752.fasta', 'RUG789.fasta', 'RUG820.fasta']
ignore_taxa1 = []
calc_stats_per_rank(path1, true_path1, ranks1, ignore_indices=ignore_indices1, ignore_taxa=ignore_taxa1)






            
                    



