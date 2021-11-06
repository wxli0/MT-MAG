"""
Calculates the precision, recall, incorrect rate, partial recall, \
    rejection rate at different levels for MT-MAG classificaton result \
        in HGR/GTDB-prediction-full-path.csv.

No command line arguments are required.
"""

import pandas as pd


def calc_stats(path, ranks, ignore_taxa =[], ignore_indices = []):
    """
    Calculates the precision, recall, incorrect rate, partial recall, \
        rejection rate at different levels for MT-MAG classificaton result.
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
        true_label = str(row['gtdb-tk-'+ranks[-1]])
        if true_label== 's__':
            continue
        if row['genus'] in ignore_taxa \
            or row['family'] in ignore_taxa:
            continue
        predicted_label  = str(row[ranks[-1]])
        # 'reject' is in prediction
        if 'reject' in predicted_label or predicted_label == 'nan':
            rejected += 1
            correct_rank = 0
            # find the rejected label
            for rank in ranks:
                pred_rank = 'gtdb-tk-'+rank
                true_rank_label = str(row[pred_rank])
                pred_rank_label = str(row[rank])
                # print("true_rank_label is:", true_rank_label)
                # print("pred_rank_label is:", pred_rank_label)
                if 'reject' in pred_rank_label:
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
            if 'reject' in str(df.loc[index][r]):
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




print("====== GTDB result ======")
path1 = "./outputs-GTDB-r202/GTDB-r202-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_indices1 =  ['RUG005.fasta', 'RUG013.fasta', 'RUG014.fasta', 'RUG023.fasta', 'RUG024.fasta', 'RUG032.fasta', 'RUG033.fasta', 'RUG039.fasta', 'RUG040.fasta', 'RUG065.fasta', 'RUG066.fasta', 'RUG068.fasta', 'RUG077.fasta', 'RUG084.fasta', 'RUG100.fasta', 'RUG114.fasta', 'RUG146.fasta', 'RUG147.fasta', 'RUG159.fasta', 'RUG162.fasta', 'RUG188.fasta', 'RUG240.fasta', 'RUG284.fasta', 'RUG287.fasta', 'RUG293.fasta', 'RUG298.fasta', 'RUG334.fasta', 'RUG347.fasta', 'RUG350.fasta', 'RUG369.fasta', 'RUG399.fasta', 'RUG428.fasta', 'RUG491.fasta', 'RUG513.fasta', 'RUG520.fasta', 'RUG574.fasta', 'RUG612.fasta', 'RUG616.fasta', 'RUG630.fasta', 'RUG632.fasta', 'RUG635.fasta', 'RUG658.fasta', 'RUG664.fasta', 'RUG673.fasta', 'RUG677.fasta', 'RUG678.fasta', 'RUG684.fasta', 'RUG686.fasta', 'RUG687.fasta', 'RUG701.fasta', 'RUG702.fasta', 'RUG703.fasta', 'RUG705.fasta', 'RUG708.fasta', 'RUG712.fasta', 'RUG714.fasta', 'RUG730.fasta', 'RUG731.fasta', 'RUG732.fasta', 'RUG752.fasta', 'RUG760.fasta', 'RUG767.fasta', 'RUG789.fasta', 'RUG797.fasta', 'RUG807.fasta', 'RUG817.fasta', 'RUG820.fasta', 'RUG841.fasta', 'RUG844.fasta', 'hRUG854.fasta', 'hRUG855.fasta', 'hRUG856.fasta', 'hRUG864.fasta', 'hRUG865.fasta', 'hRUG880.fasta', 'hRUG885.fasta', 'hRUG890.fasta', 'hRUG891.fasta', 'hRUG911.fasta']
ignore_taxa1 = []
classified_acc1, absolute_acc1, adjusted_acc1, partial_acc1, rej_stats1 = \
    calc_stats(path1, ranks1, ignore_indices=ignore_indices1, ignore_taxa=ignore_taxa1)
print("classified accuracy is:", classified_acc1, "absolute accuracy is:", \
    absolute_acc1, "adjusted accuracy is:", adjusted_acc1, "partial accuracy is:", partial_acc1)
for r in rej_stats1:
    print(rej_stats1[r], "rejects at ", r)

print("====== HGR result ======")
path2 = "./outputs-HGR-r202/HGR-r202-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_indices2 = ['even_MAG-GUT1016.fa', 'even_MAG-GUT1024.fa', 'even_MAG-GUT10262.fa', 'even_MAG-GUT1029.fa', 'even_MAG-GUT1036.fa', 'even_MAG-GUT1037.fa', 'even_MAG-GUT10417.fa', 'even_MAG-GUT1047.fa', 'even_MAG-GUT1052.fa', 'even_MAG-GUT1055.fa', 'even_MAG-GUT10593.fa', 'even_MAG-GUT1062.fa', 'even_MAG-GUT1077.fa', 'even_MAG-GUT1088.fa', 'even_MAG-GUT11004.fa', 'even_MAG-GUT1103.fa', 'even_MAG-GUT11521.fa', 'even_MAG-GUT1160.fa', 'even_MAG-GUT11638.fa', 'even_MAG-GUT1169.fa', 'even_MAG-GUT1171.fa', 'even_MAG-GUT1173.fa', 'even_MAG-GUT1177.fa', 'even_MAG-GUT11829.fa', 'even_MAG-GUT11847.fa', 'even_MAG-GUT1196.fa', 'even_MAG-GUT1197.fa', 'even_MAG-GUT11977.fa', 'even_MAG-GUT12049.fa', 'even_MAG-GUT12063.fa', 'even_MAG-GUT12082.fa', 'even_MAG-GUT12095.fa', 'even_MAG-GUT12230.fa', 'even_MAG-GUT12257.fa', 'even_MAG-GUT1228.fa', 'even_MAG-GUT1236.fa', 'even_MAG-GUT1242.fa', 'even_MAG-GUT1244.fa', 'even_MAG-GUT1255.fa', 'even_MAG-GUT1266.fa', 'even_MAG-GUT1318.fa', 'even_MAG-GUT1319.fa', 'even_MAG-GUT1328.fa', 'even_MAG-GUT1362.fa', 'even_MAG-GUT1368.fa', 'even_MAG-GUT1377.fa', 'even_MAG-GUT1384.fa', 'even_MAG-GUT13856.fa', 'even_MAG-GUT1389.fa', 'even_MAG-GUT1396.fa', 'even_MAG-GUT1465.fa', 'even_MAG-GUT1477.fa', 'even_MAG-GUT1498.fa', 'even_MAG-GUT1511.fa', 'even_MAG-GUT1522.fa', 'even_MAG-GUT1565.fa', 'even_MAG-GUT15850.fa', 'even_MAG-GUT15880.fa', 'even_MAG-GUT16567.fa', 'even_MAG-GUT17314.fa', 'even_MAG-GUT1743.fa', 'even_MAG-GUT17776.fa', 'even_MAG-GUT18526.fa', 'even_MAG-GUT1861.fa', 'even_MAG-GUT1871.fa', 'even_MAG-GUT1875.fa', 'even_MAG-GUT1876.fa', 'even_MAG-GUT1880.fa', 'even_MAG-GUT18819.fa', 'even_MAG-GUT1885.fa', 'even_MAG-GUT1887.fa', 'even_MAG-GUT1888.fa', 'even_MAG-GUT1892.fa', 'even_MAG-GUT1895.fa', 'even_MAG-GUT1898.fa', 'even_MAG-GUT1900.fa', 'even_MAG-GUT1904.fa', 'even_MAG-GUT1906.fa', 'even_MAG-GUT1908.fa', 'even_MAG-GUT1911.fa', 'even_MAG-GUT1914.fa', 'even_MAG-GUT19428.fa', 'even_MAG-GUT1946.fa', 'even_MAG-GUT1959.fa', 'even_MAG-GUT19947.fa', 'even_MAG-GUT2019.fa', 'even_MAG-GUT2025.fa', 'even_MAG-GUT2060.fa', 'even_MAG-GUT2139.fa', 'even_MAG-GUT21953.fa', 'even_MAG-GUT22420.fa', 'even_MAG-GUT22606.fa', 'even_MAG-GUT22830.fa', 'even_MAG-GUT22878.fa', 'even_MAG-GUT23613.fa', 'even_MAG-GUT23890.fa', 'even_MAG-GUT24211.fa', 'even_MAG-GUT24765.fa', 'even_MAG-GUT26303.fa', 'even_MAG-GUT26531.fa', 'even_MAG-GUT271.fa', 'even_MAG-GUT27420.fa', 'even_MAG-GUT27437.fa', 'even_MAG-GUT27453.fa', 'even_MAG-GUT28136.fa', 'even_MAG-GUT2841.fa', 'even_MAG-GUT28570.fa', 'even_MAG-GUT2873.fa', 'even_MAG-GUT28915.fa', 'even_MAG-GUT29051.fa', 'even_MAG-GUT29076.fa', 'even_MAG-GUT3231.fa', 'even_MAG-GUT3233.fa', 'even_MAG-GUT33914.fa', 'even_MAG-GUT3427.fa', 'even_MAG-GUT3435.fa', 'even_MAG-GUT3477.fa', 'even_MAG-GUT3478.fa', 'even_MAG-GUT3479.fa', 'even_MAG-GUT3531.fa', 'even_MAG-GUT3548.fa', 'even_MAG-GUT3561.fa', 'even_MAG-GUT35789.fa', 'even_MAG-GUT36009.fa', 'even_MAG-GUT36027.fa', 'even_MAG-GUT36103.fa', 'even_MAG-GUT36772.fa', 'even_MAG-GUT36794.fa', 'even_MAG-GUT36799.fa', 'even_MAG-GUT37961.fa', 'even_MAG-GUT39998.fa', 'even_MAG-GUT40025.fa', 'even_MAG-GUT40033.fa', 'even_MAG-GUT40857.fa', 'even_MAG-GUT41.fa', 'even_MAG-GUT41817.fa', 'even_MAG-GUT41924.fa', 'even_MAG-GUT42485.fa', 'even_MAG-GUT42494.fa', 'even_MAG-GUT42584.fa', 'even_MAG-GUT42613.fa', 'even_MAG-GUT43216.fa', 'even_MAG-GUT43258.fa', 'even_MAG-GUT43425.fa', 'even_MAG-GUT43440.fa', 'even_MAG-GUT43446.fa', 'even_MAG-GUT43457.fa', 'even_MAG-GUT43462.fa', 'even_MAG-GUT43463.fa', 'even_MAG-GUT43483.fa', 'even_MAG-GUT43573.fa', 'even_MAG-GUT43577.fa', 'even_MAG-GUT43620.fa', 'even_MAG-GUT43751.fa', 'even_MAG-GUT43773.fa', 'even_MAG-GUT43894.fa', 'even_MAG-GUT43943.fa', 'even_MAG-GUT44111.fa', 'even_MAG-GUT44112.fa', 'even_MAG-GUT44177.fa', 'even_MAG-GUT44433.fa', 'even_MAG-GUT44539.fa', 'even_MAG-GUT44544.fa', 'even_MAG-GUT44617.fa', 'even_MAG-GUT44851.fa', 'even_MAG-GUT45331.fa', 'even_MAG-GUT45607.fa', 'even_MAG-GUT45882.fa', 'even_MAG-GUT46037.fa', 'even_MAG-GUT46219.fa', 'even_MAG-GUT46265.fa', 'even_MAG-GUT46354.fa', 'even_MAG-GUT46437.fa', 'even_MAG-GUT46441.fa', 'even_MAG-GUT46496.fa', 'even_MAG-GUT46649.fa', 'even_MAG-GUT46722.fa', 'even_MAG-GUT46868.fa', 'even_MAG-GUT46923.fa', 'even_MAG-GUT46962.fa', 'even_MAG-GUT47106.fa', 'even_MAG-GUT47179.fa', 'even_MAG-GUT47531.fa', 'even_MAG-GUT48218.fa', 'even_MAG-GUT48445.fa', 'even_MAG-GUT48488.fa', 'even_MAG-GUT48498.fa', 'even_MAG-GUT48566.fa', 'even_MAG-GUT48585.fa', 'even_MAG-GUT48612.fa', 'even_MAG-GUT48673.fa', 'even_MAG-GUT48686.fa', 'even_MAG-GUT48704.fa', 'even_MAG-GUT48723.fa', 'even_MAG-GUT48749.fa', 'even_MAG-GUT48754.fa', 'even_MAG-GUT48761.fa', 'even_MAG-GUT48773.fa', 'even_MAG-GUT48798.fa', 'even_MAG-GUT48804.fa', 'even_MAG-GUT48829.fa', 'even_MAG-GUT48834.fa', 'even_MAG-GUT48894.fa', 'even_MAG-GUT48926.fa', 'even_MAG-GUT48968.fa', 'even_MAG-GUT48971.fa', 'even_MAG-GUT48976.fa', 'even_MAG-GUT49004.fa', 'even_MAG-GUT49010.fa', 'even_MAG-GUT49015.fa', 'even_MAG-GUT4902.fa', 'even_MAG-GUT49023.fa', 'even_MAG-GUT49063.fa', 'even_MAG-GUT49069.fa', 'even_MAG-GUT49070.fa', 'even_MAG-GUT49075.fa', 'even_MAG-GUT49076.fa', 'even_MAG-GUT49083.fa', 'even_MAG-GUT49101.fa', 'even_MAG-GUT49107.fa', 'even_MAG-GUT49118.fa', 'even_MAG-GUT49170.fa', 'even_MAG-GUT49176.fa', 'even_MAG-GUT49226.fa', 'even_MAG-GUT49236.fa', 'even_MAG-GUT49289.fa', 'even_MAG-GUT49297.fa', 'even_MAG-GUT49302.fa', 'even_MAG-GUT49315.fa', 'even_MAG-GUT49326.fa', 'even_MAG-GUT49329.fa', 'even_MAG-GUT49356.fa', 'even_MAG-GUT49359.fa', 'even_MAG-GUT49393.fa', 'even_MAG-GUT49403.fa', 'even_MAG-GUT49409.fa', 'even_MAG-GUT4942.fa', 'even_MAG-GUT49445.fa', 'even_MAG-GUT49456.fa', 'even_MAG-GUT49458.fa', 'even_MAG-GUT49469.fa', 'even_MAG-GUT49487.fa', 'even_MAG-GUT49499.fa', 'even_MAG-GUT49512.fa', 'even_MAG-GUT49529.fa', 'even_MAG-GUT49535.fa', 'even_MAG-GUT49539.fa', 'even_MAG-GUT49541.fa', 'even_MAG-GUT49542.fa', 'even_MAG-GUT49574.fa', 'even_MAG-GUT49593.fa', 'even_MAG-GUT49599.fa', 'even_MAG-GUT49609.fa', 'even_MAG-GUT49616.fa', 'even_MAG-GUT52094.fa', 'even_MAG-GUT52107.fa', 'even_MAG-GUT52138.fa', 'even_MAG-GUT53065.fa', 'even_MAG-GUT53617.fa', 'even_MAG-GUT54831.fa', 'even_MAG-GUT54931.fa', 'even_MAG-GUT56345.fa', 'even_MAG-GUT56425.fa', 'even_MAG-GUT57264.fa', 'even_MAG-GUT5727.fa', 'even_MAG-GUT57442.fa', 'even_MAG-GUT57658.fa', 'even_MAG-GUT57690.fa', 'even_MAG-GUT58014.fa', 'even_MAG-GUT58077.fa', 'even_MAG-GUT58318.fa', 'even_MAG-GUT58392.fa', 'even_MAG-GUT59039.fa', 'even_MAG-GUT5920.fa', 'even_MAG-GUT59590.fa', 'even_MAG-GUT60365.fa', 'even_MAG-GUT60874.fa', 'even_MAG-GUT61159.fa', 'even_MAG-GUT61176.fa', 'even_MAG-GUT61416.fa', 'even_MAG-GUT61880.fa', 'even_MAG-GUT61959.fa', 'even_MAG-GUT62206.fa', 'even_MAG-GUT6222.fa', 'even_MAG-GUT6229.fa', 'even_MAG-GUT6233.fa', 'even_MAG-GUT6238.fa', 'even_MAG-GUT6241.fa', 'even_MAG-GUT62429.fa', 'even_MAG-GUT6274.fa', 'even_MAG-GUT6291.fa', 'even_MAG-GUT65341.fa', 'even_MAG-GUT65553.fa', 'even_MAG-GUT65576.fa', 'even_MAG-GUT65588.fa', 'even_MAG-GUT66322.fa', 'even_MAG-GUT66330.fa', 'even_MAG-GUT66408.fa', 'even_MAG-GUT68043.fa', 'even_MAG-GUT68234.fa', 'even_MAG-GUT68245.fa', 'even_MAG-GUT68537.fa', 'even_MAG-GUT68542.fa', 'even_MAG-GUT68598.fa', 'even_MAG-GUT68629.fa', 'even_MAG-GUT68858.fa', 'even_MAG-GUT69501.fa', 'even_MAG-GUT70200.fa', 'even_MAG-GUT7062.fa', 'even_MAG-GUT70620.fa', 'even_MAG-GUT7064.fa', 'even_MAG-GUT7066.fa', 'even_MAG-GUT70664.fa', 'even_MAG-GUT7090.fa', 'even_MAG-GUT7102.fa', 'even_MAG-GUT7118.fa', 'even_MAG-GUT7121.fa', 'even_MAG-GUT7125.fa', 'even_MAG-GUT71577.fa', 'even_MAG-GUT7175.fa', 'even_MAG-GUT71751.fa', 'even_MAG-GUT7213.fa', 'even_MAG-GUT7214.fa', 'even_MAG-GUT7216.fa', 'even_MAG-GUT7222.fa', 'even_MAG-GUT7253.fa', 'even_MAG-GUT7278.fa', 'even_MAG-GUT7291.fa', 'even_MAG-GUT73376.fa', 'even_MAG-GUT73749.fa', 'even_MAG-GUT73804.fa', 'even_MAG-GUT73847.fa', 'even_MAG-GUT73862.fa', 'even_MAG-GUT74183.fa', 'even_MAG-GUT74662.fa', 'even_MAG-GUT74889.fa', 'even_MAG-GUT74895.fa', 'even_MAG-GUT7546.fa', 'even_MAG-GUT76377.fa', 'even_MAG-GUT76426.fa', 'even_MAG-GUT76486.fa', 'even_MAG-GUT76518.fa', 'even_MAG-GUT76530.fa', 'even_MAG-GUT7733.fa', 'even_MAG-GUT77471.fa', 'even_MAG-GUT77576.fa', 'even_MAG-GUT77590.fa', 'even_MAG-GUT77597.fa', 'even_MAG-GUT77615.fa', 'even_MAG-GUT77633.fa', 'even_MAG-GUT77900.fa', 'even_MAG-GUT77956.fa', 'even_MAG-GUT77982.fa', 'even_MAG-GUT78278.fa', 'even_MAG-GUT78295.fa', 'even_MAG-GUT78358.fa', 'even_MAG-GUT78410.fa', 'even_MAG-GUT78413.fa', 'even_MAG-GUT78579.fa', 'even_MAG-GUT78879.fa', 'even_MAG-GUT78908.fa', 'even_MAG-GUT78923.fa', 'even_MAG-GUT79180.fa', 'even_MAG-GUT7981.fa', 'even_MAG-GUT80685.fa', 'even_MAG-GUT80819.fa', 'even_MAG-GUT81671.fa', 'even_MAG-GUT82176.fa', 'even_MAG-GUT82203.fa', 'even_MAG-GUT8281.fa', 'even_MAG-GUT83501.fa', 'even_MAG-GUT83507.fa', 'even_MAG-GUT83922.fa', 'even_MAG-GUT83946.fa', 'even_MAG-GUT8428.fa', 'even_MAG-GUT84696.fa', 'even_MAG-GUT84793.fa', 'even_MAG-GUT85136.fa', 'even_MAG-GUT8521.fa', 'even_MAG-GUT85568.fa', 'even_MAG-GUT85881.fa', 'even_MAG-GUT85906.fa', 'even_MAG-GUT85926.fa', 'even_MAG-GUT86439.fa', 'even_MAG-GUT86514.fa', 'even_MAG-GUT86727.fa', 'even_MAG-GUT86868.fa', 'even_MAG-GUT87091.fa', 'even_MAG-GUT87486.fa', 'even_MAG-GUT87573.fa', 'even_MAG-GUT87828.fa', 'even_MAG-GUT88085.fa', 'even_MAG-GUT88218.fa', 'even_MAG-GUT88257.fa', 'even_MAG-GUT88679.fa', 'even_MAG-GUT88862.fa', 'even_MAG-GUT89162.fa', 'even_MAG-GUT89246.fa', 'even_MAG-GUT89291.fa', 'even_MAG-GUT89323.fa', 'even_MAG-GUT89608.fa', 'even_MAG-GUT89784.fa', 'even_MAG-GUT89815.fa', 'even_MAG-GUT89852.fa', 'even_MAG-GUT90020.fa', 'even_MAG-GUT90054.fa', 'even_MAG-GUT90190.fa', 'even_MAG-GUT90362.fa', 'even_MAG-GUT90441.fa', 'even_MAG-GUT90614.fa', 'even_MAG-GUT90671.fa', 'even_MAG-GUT90675.fa', 'even_MAG-GUT90682.fa', 'even_MAG-GUT90730.fa', 'even_MAG-GUT90775.fa', 'even_MAG-GUT9085.fa', 'even_MAG-GUT9090.fa', 'even_MAG-GUT90941.fa', 'even_MAG-GUT90947.fa', 'even_MAG-GUT90963.fa', 'even_MAG-GUT90995.fa', 'even_MAG-GUT91014.fa', 'even_MAG-GUT91192.fa', 'even_MAG-GUT91196.fa', 'even_MAG-GUT91251.fa', 'even_MAG-GUT91262.fa', 'even_MAG-GUT91264.fa', 'even_MAG-GUT91267.fa', 'even_MAG-GUT91272.fa', 'even_MAG-GUT91297.fa', 'even_MAG-GUT91303.fa', 'even_MAG-GUT91320.fa', 'even_MAG-GUT91328.fa', 'even_MAG-GUT91330.fa', 'even_MAG-GUT91385.fa', 'even_MAG-GUT91468.fa', 'even_MAG-GUT91470.fa', 'even_MAG-GUT91486.fa', 'even_MAG-GUT91490.fa', 'even_MAG-GUT91491.fa', 'even_MAG-GUT91492.fa', 'even_MAG-GUT91496.fa', 'even_MAG-GUT91520.fa', 'even_MAG-GUT91536.fa', 'even_MAG-GUT91546.fa', 'even_MAG-GUT91566.fa', 'even_MAG-GUT91568.fa', 'even_MAG-GUT91702.fa', 'even_MAG-GUT91712.fa', 'even_MAG-GUT91717.fa', 'even_MAG-GUT91736.fa', 'even_MAG-GUT91762.fa', 'even_MAG-GUT91779.fa', 'even_MAG-GUT91815.fa', 'even_MAG-GUT91818.fa', 'even_MAG-GUT91821.fa', 'even_MAG-GUT91823.fa', 'even_MAG-GUT91833.fa', 'even_MAG-GUT91860.fa', 'even_MAG-GUT91882.fa', 'even_MAG-GUT91886.fa', 'even_MAG-GUT91898.fa', 'even_MAG-GUT91911.fa', 'even_MAG-GUT91912.fa', 'even_MAG-GUT91923.fa', 'even_MAG-GUT91926.fa', 'even_MAG-GUT91932.fa', 'even_MAG-GUT91941.fa', 'even_MAG-GUT91943.fa', 'even_MAG-GUT91954.fa', 'even_MAG-GUT91960.fa', 'even_MAG-GUT92006.fa', 'even_MAG-GUT92066.fa', 'even_MAG-GUT92111.fa', 'even_MAG-GUT9303.fa', 'even_MAG-GUT9316.fa', 'even_MAG-GUT9364.fa', 'even_MAG-GUT9376.fa', 'even_MAG-GUT940.fa', 'even_MAG-GUT945.fa', 'even_MAG-GUT9681.fa', 'even_MAG-GUT9766.fa', 'even_MAG-GUT984.fa']
ignore_taxa2 = ['f__Lachnospiraceae', 'f__Burkholderiaceae', 'g__Prevotella']
classified_acc2, absolute_acc2, adjusted_acc2, partial_acc2, rej_stats2 = \
    calc_stats(path2, ranks2, ignore_indices=ignore_indices2, ignore_taxa=ignore_taxa2)

print("classified accuracy is:", classified_acc2, "absolute accuracy is:", \
    absolute_acc2, "adjusted accuracy is:", adjusted_acc2, "partial accuracy is:", partial_acc2)
for r in rej_stats2:
    print(rej_stats2[r], "rejects at ", r)





            
                    



