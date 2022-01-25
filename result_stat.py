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
path2 = "./outputs-HGR-r202-archive3/HGR-r202-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_indices2 = ['MAG-GUT1016.fa', 'MAG-GUT1024.fa', 'MAG-GUT10262.fa', 'MAG-GUT1029.fa', 'MAG-GUT1036.fa', 'MAG-GUT1037.fa', 'MAG-GUT10417.fa', 'MAG-GUT1047.fa', 'MAG-GUT1052.fa', 'MAG-GUT1055.fa', 'MAG-GUT10593.fa', 'MAG-GUT1062.fa', 'MAG-GUT1077.fa', 'MAG-GUT1088.fa', 'MAG-GUT11004.fa', 'MAG-GUT1103.fa', 'MAG-GUT11521.fa', 'MAG-GUT1160.fa', 'MAG-GUT11638.fa', 'MAG-GUT1169.fa', 'MAG-GUT1171.fa', 'MAG-GUT1173.fa', 'MAG-GUT1177.fa', 'MAG-GUT11829.fa', 'MAG-GUT11847.fa', 'MAG-GUT1196.fa', 'MAG-GUT1197.fa', 'MAG-GUT11977.fa', 'MAG-GUT12049.fa', 'MAG-GUT12063.fa', 'MAG-GUT12082.fa', 'MAG-GUT12095.fa', 'MAG-GUT12230.fa', 'MAG-GUT12257.fa', 'MAG-GUT1228.fa', 'MAG-GUT1236.fa', 'MAG-GUT1242.fa', 'MAG-GUT1244.fa', 'MAG-GUT1255.fa', 'MAG-GUT1266.fa', 'MAG-GUT1318.fa', 'MAG-GUT1319.fa', 'MAG-GUT1328.fa', 'MAG-GUT1362.fa', 'MAG-GUT1368.fa', 'MAG-GUT1377.fa', 'MAG-GUT1384.fa', 'MAG-GUT13856.fa', 'MAG-GUT1389.fa', 'MAG-GUT1396.fa', 'MAG-GUT1465.fa', 'MAG-GUT1477.fa', 'MAG-GUT1498.fa', 'MAG-GUT1511.fa', 'MAG-GUT1522.fa', 'MAG-GUT1565.fa', 'MAG-GUT15850.fa', 'MAG-GUT15880.fa', 'MAG-GUT16567.fa', 'MAG-GUT17314.fa', 'MAG-GUT1743.fa', 'MAG-GUT17776.fa', 'MAG-GUT18526.fa', 'MAG-GUT1861.fa', 'MAG-GUT1871.fa', 'MAG-GUT1875.fa', 'MAG-GUT1876.fa', 'MAG-GUT1880.fa', 'MAG-GUT18819.fa', 'MAG-GUT1885.fa', 'MAG-GUT1887.fa', 'MAG-GUT1888.fa', 'MAG-GUT1892.fa', 'MAG-GUT1895.fa', 'MAG-GUT1898.fa', 'MAG-GUT1900.fa', 'MAG-GUT1904.fa', 'MAG-GUT1906.fa', 'MAG-GUT1908.fa', 'MAG-GUT1911.fa', 'MAG-GUT1914.fa', 'MAG-GUT19428.fa', 'MAG-GUT1946.fa', 'MAG-GUT1959.fa', 'MAG-GUT19947.fa', 'MAG-GUT2019.fa', 'MAG-GUT2025.fa', 'MAG-GUT2060.fa', 'MAG-GUT2139.fa', 'MAG-GUT21953.fa', 'MAG-GUT22420.fa', 'MAG-GUT22606.fa', 'MAG-GUT22830.fa', 'MAG-GUT22878.fa', 'MAG-GUT23613.fa', 'MAG-GUT23890.fa', 'MAG-GUT24211.fa', 'MAG-GUT24765.fa', 'MAG-GUT26303.fa', 'MAG-GUT26531.fa', 'MAG-GUT271.fa', 'MAG-GUT27420.fa', 'MAG-GUT27437.fa', 'MAG-GUT27453.fa', 'MAG-GUT28136.fa', 'MAG-GUT2841.fa', 'MAG-GUT28570.fa', 'MAG-GUT2873.fa', 'MAG-GUT28915.fa', 'MAG-GUT29051.fa', 'MAG-GUT29076.fa', 'MAG-GUT3231.fa', 'MAG-GUT3233.fa', 'MAG-GUT33914.fa', 'MAG-GUT3427.fa', 'MAG-GUT3435.fa', 'MAG-GUT3477.fa', 'MAG-GUT3478.fa', 'MAG-GUT3479.fa', 'MAG-GUT3531.fa', 'MAG-GUT3548.fa', 'MAG-GUT3561.fa', 'MAG-GUT35789.fa', 'MAG-GUT36009.fa', 'MAG-GUT36027.fa', 'MAG-GUT36103.fa', 'MAG-GUT36772.fa', 'MAG-GUT36794.fa', 'MAG-GUT36799.fa', 'MAG-GUT37961.fa', 'MAG-GUT39998.fa', 'MAG-GUT40025.fa', 'MAG-GUT40033.fa', 'MAG-GUT40857.fa', 'MAG-GUT41.fa', 'MAG-GUT41817.fa', 'MAG-GUT41924.fa', 'MAG-GUT42485.fa', 'MAG-GUT42494.fa', 'MAG-GUT42584.fa', 'MAG-GUT42613.fa', 'MAG-GUT43216.fa', 'MAG-GUT43258.fa', 'MAG-GUT43425.fa', 'MAG-GUT43440.fa', 'MAG-GUT43446.fa', 'MAG-GUT43457.fa', 'MAG-GUT43462.fa', 'MAG-GUT43463.fa', 'MAG-GUT43483.fa', 'MAG-GUT43573.fa', 'MAG-GUT43577.fa', 'MAG-GUT43620.fa', 'MAG-GUT43751.fa', 'MAG-GUT43773.fa', 'MAG-GUT43894.fa', 'MAG-GUT43943.fa', 'MAG-GUT44111.fa', 'MAG-GUT44112.fa', 'MAG-GUT44177.fa', 'MAG-GUT44433.fa', 'MAG-GUT44539.fa', 'MAG-GUT44544.fa', 'MAG-GUT44617.fa', 'MAG-GUT44851.fa', 'MAG-GUT45331.fa', 'MAG-GUT45607.fa', 'MAG-GUT45882.fa', 'MAG-GUT46037.fa', 'MAG-GUT46219.fa', 'MAG-GUT46265.fa', 'MAG-GUT46354.fa', 'MAG-GUT46437.fa', 'MAG-GUT46441.fa', 'MAG-GUT46496.fa', 'MAG-GUT46649.fa', 'MAG-GUT46722.fa', 'MAG-GUT46868.fa', 'MAG-GUT46923.fa', 'MAG-GUT46962.fa', 'MAG-GUT47106.fa', 'MAG-GUT47179.fa', 'MAG-GUT47531.fa', 'MAG-GUT48218.fa', 'MAG-GUT48445.fa', 'MAG-GUT48488.fa', 'MAG-GUT48498.fa', 'MAG-GUT48566.fa', 'MAG-GUT48585.fa', 'MAG-GUT48612.fa', 'MAG-GUT48673.fa', 'MAG-GUT48686.fa', 'MAG-GUT48704.fa', 'MAG-GUT48723.fa', 'MAG-GUT48749.fa', 'MAG-GUT48754.fa', 'MAG-GUT48761.fa', 'MAG-GUT48773.fa', 'MAG-GUT48798.fa', 'MAG-GUT48804.fa', 'MAG-GUT48829.fa', 'MAG-GUT48834.fa', 'MAG-GUT48894.fa', 'MAG-GUT48926.fa', 'MAG-GUT48968.fa', 'MAG-GUT48971.fa', 'MAG-GUT48976.fa', 'MAG-GUT49004.fa', 'MAG-GUT49010.fa', 'MAG-GUT49015.fa', 'MAG-GUT4902.fa', 'MAG-GUT49023.fa', 'MAG-GUT49063.fa', 'MAG-GUT49069.fa', 'MAG-GUT49070.fa', 'MAG-GUT49075.fa', 'MAG-GUT49076.fa', 'MAG-GUT49083.fa', 'MAG-GUT49101.fa', 'MAG-GUT49107.fa', 'MAG-GUT49118.fa', 'MAG-GUT49170.fa', 'MAG-GUT49176.fa', 'MAG-GUT49226.fa', 'MAG-GUT49236.fa', 'MAG-GUT49289.fa', 'MAG-GUT49297.fa', 'MAG-GUT49302.fa', 'MAG-GUT49315.fa', 'MAG-GUT49326.fa', 'MAG-GUT49329.fa', 'MAG-GUT49356.fa', 'MAG-GUT49359.fa', 'MAG-GUT49393.fa', 'MAG-GUT49403.fa', 'MAG-GUT49409.fa', 'MAG-GUT4942.fa', 'MAG-GUT49445.fa', 'MAG-GUT49456.fa', 'MAG-GUT49458.fa', 'MAG-GUT49469.fa', 'MAG-GUT49487.fa', 'MAG-GUT49499.fa', 'MAG-GUT49512.fa', 'MAG-GUT49529.fa', 'MAG-GUT49535.fa', 'MAG-GUT49539.fa', 'MAG-GUT49541.fa', 'MAG-GUT49542.fa', 'MAG-GUT49574.fa', 'MAG-GUT49593.fa', 'MAG-GUT49599.fa', 'MAG-GUT49609.fa', 'MAG-GUT49616.fa', 'MAG-GUT52094.fa', 'MAG-GUT52107.fa', 'MAG-GUT52138.fa', 'MAG-GUT53065.fa', 'MAG-GUT53617.fa', 'MAG-GUT54831.fa', 'MAG-GUT54931.fa', 'MAG-GUT56345.fa', 'MAG-GUT56425.fa', 'MAG-GUT57264.fa', 'MAG-GUT5727.fa', 'MAG-GUT57442.fa', 'MAG-GUT57658.fa', 'MAG-GUT57690.fa', 'MAG-GUT58014.fa', 'MAG-GUT58077.fa', 'MAG-GUT58318.fa', 'MAG-GUT58392.fa', 'MAG-GUT59039.fa', 'MAG-GUT5920.fa', 'MAG-GUT59590.fa', 'MAG-GUT60365.fa', 'MAG-GUT60874.fa', 'MAG-GUT61159.fa', 'MAG-GUT61176.fa', 'MAG-GUT61416.fa', 'MAG-GUT61880.fa', 'MAG-GUT61959.fa', 'MAG-GUT62206.fa', 'MAG-GUT6222.fa', 'MAG-GUT6229.fa', 'MAG-GUT6233.fa', 'MAG-GUT6238.fa', 'MAG-GUT6241.fa', 'MAG-GUT62429.fa', 'MAG-GUT6274.fa', 'MAG-GUT6291.fa', 'MAG-GUT65341.fa', 'MAG-GUT65553.fa', 'MAG-GUT65576.fa', 'MAG-GUT65588.fa', 'MAG-GUT66322.fa', 'MAG-GUT66330.fa', 'MAG-GUT66408.fa', 'MAG-GUT68043.fa', 'MAG-GUT68234.fa', 'MAG-GUT68245.fa', 'MAG-GUT68537.fa', 'MAG-GUT68542.fa', 'MAG-GUT68598.fa', 'MAG-GUT68629.fa', 'MAG-GUT68858.fa', 'MAG-GUT69501.fa', 'MAG-GUT70200.fa', 'MAG-GUT7062.fa', 'MAG-GUT70620.fa', 'MAG-GUT7064.fa', 'MAG-GUT7066.fa', 'MAG-GUT70664.fa', 'MAG-GUT7090.fa', 'MAG-GUT7102.fa', 'MAG-GUT7118.fa', 'MAG-GUT7121.fa', 'MAG-GUT7125.fa', 'MAG-GUT71577.fa', 'MAG-GUT7175.fa', 'MAG-GUT71751.fa', 'MAG-GUT7213.fa', 'MAG-GUT7214.fa', 'MAG-GUT7216.fa', 'MAG-GUT7222.fa', 'MAG-GUT7253.fa', 'MAG-GUT7278.fa', 'MAG-GUT7291.fa', 'MAG-GUT73376.fa', 'MAG-GUT73749.fa', 'MAG-GUT73804.fa', 'MAG-GUT73847.fa', 'MAG-GUT73862.fa', 'MAG-GUT74183.fa', 'MAG-GUT74662.fa', 'MAG-GUT74889.fa', 'MAG-GUT74895.fa', 'MAG-GUT7546.fa', 'MAG-GUT76377.fa', 'MAG-GUT76426.fa', 'MAG-GUT76486.fa', 'MAG-GUT76518.fa', 'MAG-GUT76530.fa', 'MAG-GUT7733.fa', 'MAG-GUT77471.fa', 'MAG-GUT77576.fa', 'MAG-GUT77590.fa', 'MAG-GUT77597.fa', 'MAG-GUT77615.fa', 'MAG-GUT77633.fa', 'MAG-GUT77900.fa', 'MAG-GUT77956.fa', 'MAG-GUT77982.fa', 'MAG-GUT78278.fa', 'MAG-GUT78295.fa', 'MAG-GUT78358.fa', 'MAG-GUT78410.fa', 'MAG-GUT78413.fa', 'MAG-GUT78579.fa', 'MAG-GUT78879.fa', 'MAG-GUT78908.fa', 'MAG-GUT78923.fa', 'MAG-GUT79180.fa', 'MAG-GUT7981.fa', 'MAG-GUT80685.fa', 'MAG-GUT80819.fa', 'MAG-GUT81671.fa', 'MAG-GUT82176.fa', 'MAG-GUT82203.fa', 'MAG-GUT8281.fa', 'MAG-GUT83501.fa', 'MAG-GUT83507.fa', 'MAG-GUT83922.fa', 'MAG-GUT83946.fa', 'MAG-GUT8428.fa', 'MAG-GUT84696.fa', 'MAG-GUT84793.fa', 'MAG-GUT85136.fa', 'MAG-GUT8521.fa', 'MAG-GUT85568.fa', 'MAG-GUT85881.fa', 'MAG-GUT85906.fa', 'MAG-GUT85926.fa', 'MAG-GUT86439.fa', 'MAG-GUT86514.fa', 'MAG-GUT86727.fa', 'MAG-GUT86868.fa', 'MAG-GUT87091.fa', 'MAG-GUT87486.fa', 'MAG-GUT87573.fa', 'MAG-GUT87828.fa', 'MAG-GUT88085.fa', 'MAG-GUT88218.fa', 'MAG-GUT88257.fa', 'MAG-GUT88679.fa', 'MAG-GUT88862.fa', 'MAG-GUT89162.fa', 'MAG-GUT89246.fa', 'MAG-GUT89291.fa', 'MAG-GUT89323.fa', 'MAG-GUT89608.fa', 'MAG-GUT89784.fa', 'MAG-GUT89815.fa', 'MAG-GUT89852.fa', 'MAG-GUT90020.fa', 'MAG-GUT90054.fa', 'MAG-GUT90190.fa', 'MAG-GUT90362.fa', 'MAG-GUT90441.fa', 'MAG-GUT90614.fa', 'MAG-GUT90671.fa', 'MAG-GUT90675.fa', 'MAG-GUT90682.fa', 'MAG-GUT90730.fa', 'MAG-GUT90775.fa', 'MAG-GUT9085.fa', 'MAG-GUT9090.fa', 'MAG-GUT90941.fa', 'MAG-GUT90947.fa', 'MAG-GUT90963.fa', 'MAG-GUT90995.fa', 'MAG-GUT91014.fa', 'MAG-GUT91192.fa', 'MAG-GUT91196.fa', 'MAG-GUT91251.fa', 'MAG-GUT91262.fa', 'MAG-GUT91264.fa', 'MAG-GUT91267.fa', 'MAG-GUT91272.fa', 'MAG-GUT91297.fa', 'MAG-GUT91303.fa', 'MAG-GUT91320.fa', 'MAG-GUT91328.fa', 'MAG-GUT91330.fa', 'MAG-GUT91385.fa', 'MAG-GUT91468.fa', 'MAG-GUT91470.fa', 'MAG-GUT91486.fa', 'MAG-GUT91490.fa', 'MAG-GUT91491.fa', 'MAG-GUT91492.fa', 'MAG-GUT91496.fa', 'MAG-GUT91520.fa', 'MAG-GUT91536.fa', 'MAG-GUT91546.fa', 'MAG-GUT91566.fa', 'MAG-GUT91568.fa', 'MAG-GUT91702.fa', 'MAG-GUT91712.fa', 'MAG-GUT91717.fa', 'MAG-GUT91736.fa', 'MAG-GUT91762.fa', 'MAG-GUT91779.fa', 'MAG-GUT91815.fa', 'MAG-GUT91818.fa', 'MAG-GUT91821.fa', 'MAG-GUT91823.fa', 'MAG-GUT91833.fa', 'MAG-GUT91860.fa', 'MAG-GUT91882.fa', 'MAG-GUT91886.fa', 'MAG-GUT91898.fa', 'MAG-GUT91911.fa', 'MAG-GUT91912.fa', 'MAG-GUT91923.fa', 'MAG-GUT91926.fa', 'MAG-GUT91932.fa', 'MAG-GUT91941.fa', 'MAG-GUT91943.fa', 'MAG-GUT91954.fa', 'MAG-GUT91960.fa', 'MAG-GUT92006.fa', 'MAG-GUT92066.fa', 'MAG-GUT92111.fa', 'MAG-GUT9303.fa', 'MAG-GUT9316.fa', 'MAG-GUT9364.fa', 'MAG-GUT9376.fa', 'MAG-GUT940.fa', 'MAG-GUT945.fa', 'MAG-GUT9681.fa', 'MAG-GUT9766.fa', 'MAG-GUT984.fa']
# ignore_taxa2 = ['o__Lachnospirales', 'f__Ruminococcaceae', 'f__Oscillospiraceae', 'g__Prevotella']
calc_stats_per_rank(path2, path_true2, ranks2, ignore_indices=ignore_indices2, ignore_taxa=[])


print("====== GTDB result ======")
true_path1 = "./outputs-GTDB-r202-archive1/GTDB-r202-prediction-full-path.csv"
path1 = "~/Desktop/GTDB-r202-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_indices1 =  ['RUG005.fasta', 'RUG013.fasta', 'RUG014.fasta', 'RUG023.fasta', 'RUG024.fasta', 'RUG032.fasta', 'RUG033.fasta', 'RUG039.fasta', 'RUG040.fasta', 'RUG065.fasta', 'RUG066.fasta', 'RUG068.fasta', 'RUG077.fasta', 'RUG084.fasta', 'RUG100.fasta', 'RUG114.fasta', 'RUG146.fasta', 'RUG147.fasta', 'RUG159.fasta', 'RUG162.fasta', 'RUG188.fasta', 'RUG240.fasta', 'RUG284.fasta', 'RUG287.fasta', 'RUG293.fasta', 'RUG298.fasta', 'RUG334.fasta', 'RUG347.fasta', 'RUG350.fasta', 'RUG369.fasta', 'RUG399.fasta', 'RUG428.fasta', 'RUG491.fasta', 'RUG513.fasta', 'RUG520.fasta', 'RUG574.fasta', 'RUG612.fasta', 'RUG616.fasta', 'RUG630.fasta', 'RUG632.fasta', 'RUG635.fasta', 'RUG658.fasta', 'RUG664.fasta', 'RUG673.fasta', 'RUG677.fasta', 'RUG678.fasta', 'RUG684.fasta', 'RUG686.fasta', 'RUG687.fasta', 'RUG701.fasta', 'RUG702.fasta', 'RUG703.fasta', 'RUG705.fasta', 'RUG708.fasta', 'RUG712.fasta', 'RUG714.fasta', 'RUG730.fasta', 'RUG731.fasta', 'RUG732.fasta', 'RUG752.fasta', 'RUG760.fasta', 'RUG767.fasta', 'RUG789.fasta', 'RUG797.fasta', 'RUG807.fasta', 'RUG817.fasta', 'RUG820.fasta', 'RUG841.fasta', 'RUG844.fasta', 'hRUG854.fasta', 'hRUG855.fasta', 'hRUG856.fasta', 'hRUG864.fasta', 'hRUG865.fasta', 'hRUG880.fasta', 'hRUG885.fasta', 'hRUG890.fasta', 'hRUG891.fasta', 'hRUG911.fasta']
ignore_taxa1 = []
calc_stats_per_rank(path1, true_path1, ranks1, ignore_indices=ignore_indices1, ignore_taxa=ignore_taxa1)






            
                    



