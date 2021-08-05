import os
import pandas as pd


# calculates the precision, recall, incorrect rate, partial recall, rejection rate at different levels
def calc_stats(path, ranks, ignore_taxons =[], ignore_indices = []):
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

    for index, row in df.iterrows():
        # print(index)
        if index in ignore_indices:
            continue
        if df.loc[index]['gtdb-tk-species'] == 's__':
            continue
        if df.loc[index]['genus'] in ignore_taxons:
            continue
        for i in range(len(ranks)):
            cur_rank = ranks[i]
            cur_pred = str(df.loc[index][cur_rank])
            label_rank = "gtdb-tk-"+cur_rank
            label_pred = str(df.loc[index][label_rank])
            pre_rank = ranks[i-1]
            pre_pred = str(df.loc[index][pre_rank])
            pre_label_rank = "gtdb-tk-"+pre_rank
            pre_label_pred = str(df.loc[index][pre_label_rank])
            if cur_rank == ranks[-1] and cur_pred == label_pred:
                partial_correct += 1
                correct += 1
                total += 1
                break
            elif (cur_rank != ranks[0] and 'reject' in cur_pred and pre_pred == pre_label_pred) \
                or cur_rank == ranks[0] and 'reject' in cur_pred:
                partial_correct += i/len(ranks)
                total += 1
                rejected += 1
                break
            elif cur_pred != label_pred and cur_pred != 'nan':
                incorrect += 1
                total += 1
                break

    for index, row in df.iterrows():
        for r in ranks:
            if 'reject' in str(df.loc[index][r]):
                rej_stats[r] += 1
                break
            
    for k in rej_stats:
        rej_stats[k] /= total
    print("total is:", total)           
    return correct/(total-rejected), correct/total, incorrect/total, partial_correct/total, rej_stats




path1 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-r202/MLDSP-prediction-full-path.csv"
ranks1 = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_indices1 = ['RUG013.fa', 'RUG014.fa', 'RUG023.fa', 'RUG024.fa', 'RUG032.fa', 'RUG033.fa', 'RUG035.fa', 'RUG038.fa', 'RUG039.fa', 'RUG040.fa', 'RUG065.fa', 'RUG066.fa', 'RUG068.fa', 'RUG077.fa', 'RUG089.fa', 'RUG100.fa', 'RUG114.fa', 'RUG118.fa', 'RUG129.fa', 'RUG130.fa', 'RUG141.fa', 'RUG146.fa', 'RUG147.fa', 'RUG162.fa', 'RUG163.fa', 'RUG171.fa', 'RUG188.fa', 'RUG190.fa', 'RUG208.fa', 'RUG238.fa', 'RUG239.fa', 'RUG240.fa', 'RUG243.fa', 'RUG255.fa', 'RUG258.fa', 'RUG260.fa', 'RUG284.fa', 'RUG287.fa', 'RUG293.fa', 'RUG298.fa', 'RUG314.fa', 'RUG334.fa', 'RUG343.fa', 'RUG347.fa', 'RUG350.fa', 'RUG351.fa', 'RUG353.fa', 'RUG361.fa', 'RUG369.fa', 'RUG399.fa', 'RUG400.fa', 'RUG408.fa', 'RUG420.fa', 'RUG428.fa', 'RUG444.fa', 'RUG466.fa', 'RUG479.fa', 'RUG486.fa', 'RUG491.fa', 'RUG508.fa', 'RUG513.fa', 'RUG517.fa', 'RUG520.fa', 'RUG524.fa', 'RUG540.fa', 'RUG555.fa', 'RUG567.fa', 'RUG570.fa', 'RUG574.fa', 'RUG596.fa', 'RUG612.fa', 'RUG621.fa', 'RUG630.fa', 'RUG635.fa', 'RUG636.fa', 'RUG642.fa', 'RUG650.fa', 'RUG652.fa', 'RUG658.fa', 'RUG661.fa', 'RUG663.fa', 'RUG664.fa', 'RUG666.fa', 'RUG675.fa', 'RUG677.fa', 'RUG678.fa', 'RUG684.fa', 'RUG686.fa', 'RUG687.fa', 'RUG701.fa', 'RUG702.fa', 'RUG703.fa', 'RUG708.fa', 'RUG714.fa', 'RUG728.fa', 'RUG730.fa', 'RUG731.fa', 'RUG732.fa', 'RUG752.fa', 'RUG754.fa', 'RUG761.fa', 'RUG767.fa', 'RUG770.fa', 'RUG789.fa', 'RUG797.fa', 'RUG803.fa', 'RUG807.fa', 'RUG808.fa', 'RUG817.fa', 'RUG820.fa', 'RUG841.fa', 'RUG844.fa', 'hRUG854.fa', 'hRUG855.fa', 'hRUG856.fa', 'hRUG862.fa', 'hRUG864.fa', 'hRUG865.fa', 'hRUG866.fa', 'hRUG881.fa', 'hRUG890.fa', 'hRUG891.fa', 'hRUG910.fa', 'hRUG911.fa']
precision1, recall1, incorrect_rate1, partial_recall1, rej_stats1 = calc_stats(path1, ranks1, ignore_indices=ignore_indices1)
print("precision is:", precision1, "recall is:", recall1, "incorrect rate is:", incorrect_rate1, "partial recall is:", partial_recall1)
for r in rej_stats1:
    print(rej_stats1[r], "rejects at ", r)
print("total rejection rate is:", sum(rej_stats1.values()))

path2 = "/Users/wanxinli/Desktop/project.nosync/BlindKameris-new/outputs-HGR-r202/HGR-prediction-full-path.csv"
ranks2 = ['phylum', 'class', 'order', 'family', 'genus', 'species']
ignore_taxons2 = ['g__Pediococcus', 'g__Ruminococcus_F', 'g__F0040']
ignore_indices2 = ['even_MAG-GUT1016', 'even_MAG-GUT10262', 'even_MAG-GUT1029', 'even_MAG-GUT1036', 'even_MAG-GUT1037', 'even_MAG-GUT1047', 'even_MAG-GUT1052', 'even_MAG-GUT1055', 'even_MAG-GUT1062', 'even_MAG-GUT1077', 'even_MAG-GUT1088', 'even_MAG-GUT11004', 'even_MAG-GUT1103', 'even_MAG-GUT11521', 'even_MAG-GUT1160', 'even_MAG-GUT11638', 'even_MAG-GUT1169', 'even_MAG-GUT1171', 'even_MAG-GUT1173', 'even_MAG-GUT1177', 'even_MAG-GUT11829', 'even_MAG-GUT11847', 'even_MAG-GUT1196', 'even_MAG-GUT1197', 'even_MAG-GUT11977', 'even_MAG-GUT12049', 'even_MAG-GUT12063', 'even_MAG-GUT12082', 'even_MAG-GUT12095', 'even_MAG-GUT12230', 'even_MAG-GUT12257', 'even_MAG-GUT1228', 'even_MAG-GUT1236', 'even_MAG-GUT1242', 'even_MAG-GUT1244', 'even_MAG-GUT1255', 'even_MAG-GUT1266', 'even_MAG-GUT1318', 'even_MAG-GUT1319', 'even_MAG-GUT1328', 'even_MAG-GUT1362', 'even_MAG-GUT1368', 'even_MAG-GUT13856', 'even_MAG-GUT1389', 'even_MAG-GUT1396', 'even_MAG-GUT14645', 'even_MAG-GUT1477', 'even_MAG-GUT1498', 'even_MAG-GUT1511', 'even_MAG-GUT1522', 'even_MAG-GUT1565', 'even_MAG-GUT15850', 'even_MAG-GUT15880', 'even_MAG-GUT17314', 'even_MAG-GUT1743', 'even_MAG-GUT17776', 'even_MAG-GUT18526', 'even_MAG-GUT1861', 'even_MAG-GUT1871', 'even_MAG-GUT1875', 'even_MAG-GUT1876', 'even_MAG-GUT1880', 'even_MAG-GUT18819', 'even_MAG-GUT1885', 'even_MAG-GUT1887', 'even_MAG-GUT1888', 'even_MAG-GUT1892', 'even_MAG-GUT1895', 'even_MAG-GUT1898', 'even_MAG-GUT1900', 'even_MAG-GUT1904', 'even_MAG-GUT1906', 'even_MAG-GUT1908', 'even_MAG-GUT1911', 'even_MAG-GUT1914', 'even_MAG-GUT19428', 'even_MAG-GUT1946', 'even_MAG-GUT1959', 'even_MAG-GUT19947', 'even_MAG-GUT2019', 'even_MAG-GUT2025', 'even_MAG-GUT2060', 'even_MAG-GUT2139', 'even_MAG-GUT21953', 'even_MAG-GUT22420', 'even_MAG-GUT22606', 'even_MAG-GUT22830', 'even_MAG-GUT23613', 'even_MAG-GUT23890', 'even_MAG-GUT24211', 'even_MAG-GUT26303', 'even_MAG-GUT26531', 'even_MAG-GUT271', 'even_MAG-GUT27420', 'even_MAG-GUT27437', 'even_MAG-GUT27453', 'even_MAG-GUT2841', 'even_MAG-GUT28570', 'even_MAG-GUT2873', 'even_MAG-GUT28915', 'even_MAG-GUT29051', 'even_MAG-GUT29076', 'even_MAG-GUT3231', 'even_MAG-GUT3233', 'even_MAG-GUT3427', 'even_MAG-GUT3435', 'even_MAG-GUT3477', 'even_MAG-GUT3479', 'even_MAG-GUT3531', 'even_MAG-GUT3548', 'even_MAG-GUT3561', 'even_MAG-GUT35789', 'even_MAG-GUT36103', 'even_MAG-GUT36772', 'even_MAG-GUT36794', 'even_MAG-GUT36799', 'even_MAG-GUT37961', 'even_MAG-GUT39998', 'even_MAG-GUT40025', 'even_MAG-GUT40033', 'even_MAG-GUT41', 'even_MAG-GUT41817', 'even_MAG-GUT42613', 'even_MAG-GUT43216', 'even_MAG-GUT43258', 'even_MAG-GUT43425', 'even_MAG-GUT43440', 'even_MAG-GUT43446', 'even_MAG-GUT43457', 'even_MAG-GUT43462', 'even_MAG-GUT43463', 'even_MAG-GUT43483', 'even_MAG-GUT43573', 'even_MAG-GUT43577', 'even_MAG-GUT43620', 'even_MAG-GUT43751', 'even_MAG-GUT43773', 'even_MAG-GUT43943', 'even_MAG-GUT44111', 'even_MAG-GUT44177', 'even_MAG-GUT44539', 'even_MAG-GUT44544', 'even_MAG-GUT44617', 'even_MAG-GUT44851', 'even_MAG-GUT45331', 'even_MAG-GUT45607', 'even_MAG-GUT45882', 'even_MAG-GUT46219', 'even_MAG-GUT46354', 'even_MAG-GUT46437', 'even_MAG-GUT46441', 'even_MAG-GUT46868', 'even_MAG-GUT46923', 'even_MAG-GUT46962', 'even_MAG-GUT47106', 'even_MAG-GUT47179', 'even_MAG-GUT47531', 'even_MAG-GUT48218', 'even_MAG-GUT48445', 'even_MAG-GUT48488', 'even_MAG-GUT48498', 'even_MAG-GUT48566', 'even_MAG-GUT48585', 'even_MAG-GUT48612', 'even_MAG-GUT48673', 'even_MAG-GUT48686', 'even_MAG-GUT48704', 'even_MAG-GUT48723', 'even_MAG-GUT48749', 'even_MAG-GUT48754', 'even_MAG-GUT48761', 'even_MAG-GUT48773', 'even_MAG-GUT48798', 'even_MAG-GUT48804', 'even_MAG-GUT48829', 'even_MAG-GUT48834', 'even_MAG-GUT48894', 'even_MAG-GUT48968', 'even_MAG-GUT48971', 'even_MAG-GUT48976', 'even_MAG-GUT49004', 'even_MAG-GUT49010', 'even_MAG-GUT49015', 'even_MAG-GUT4902', 'even_MAG-GUT49023', 'even_MAG-GUT49063', 'even_MAG-GUT49069', 'even_MAG-GUT49070', 'even_MAG-GUT49075', 'even_MAG-GUT49083', 'even_MAG-GUT49101', 'even_MAG-GUT49118', 'even_MAG-GUT49170', 'even_MAG-GUT49176', 'even_MAG-GUT49226', 'even_MAG-GUT49236', 'even_MAG-GUT49289', 'even_MAG-GUT49297', 'even_MAG-GUT49302', 'even_MAG-GUT49315', 'even_MAG-GUT49326', 'even_MAG-GUT49329', 'even_MAG-GUT49356', 'even_MAG-GUT49359', 'even_MAG-GUT49393', 'even_MAG-GUT49403', 'even_MAG-GUT49409', 'even_MAG-GUT4942', 'even_MAG-GUT49456', 'even_MAG-GUT49458', 'even_MAG-GUT49469', 'even_MAG-GUT49487', 'even_MAG-GUT49499', 'even_MAG-GUT49512', 'even_MAG-GUT49529', 'even_MAG-GUT49535', 'even_MAG-GUT49539', 'even_MAG-GUT49541', 'even_MAG-GUT49574', 'even_MAG-GUT49593', 'even_MAG-GUT49599', 'even_MAG-GUT49609', 'even_MAG-GUT49616', 'even_MAG-GUT53065', 'even_MAG-GUT53617', 'even_MAG-GUT54831', 'even_MAG-GUT54931', 'even_MAG-GUT56345', 'even_MAG-GUT56425', 'even_MAG-GUT57264', 'even_MAG-GUT57442', 'even_MAG-GUT57658', 'even_MAG-GUT57690', 'even_MAG-GUT58014', 'even_MAG-GUT58318', 'even_MAG-GUT58392', 'even_MAG-GUT59590', 'even_MAG-GUT60365', 'even_MAG-GUT60874', 'even_MAG-GUT61176', 'even_MAG-GUT61416', 'even_MAG-GUT61880', 'even_MAG-GUT62206', 'even_MAG-GUT6222', 'even_MAG-GUT6229', 'even_MAG-GUT6233', 'even_MAG-GUT6238', 'even_MAG-GUT6241', 'even_MAG-GUT62429', 'even_MAG-GUT6274', 'even_MAG-GUT6291', 'even_MAG-GUT65553', 'even_MAG-GUT65576', 'even_MAG-GUT65588', 'even_MAG-GUT66322', 'even_MAG-GUT66330', 'even_MAG-GUT66408', 'even_MAG-GUT68043', 'even_MAG-GUT68245', 'even_MAG-GUT68542', 'even_MAG-GUT68598', 'even_MAG-GUT68629', 'even_MAG-GUT68858', 'even_MAG-GUT69501', 'even_MAG-GUT70200', 'even_MAG-GUT7062', 'even_MAG-GUT70620', 'even_MAG-GUT7064', 'even_MAG-GUT7066', 'even_MAG-GUT70664', 'even_MAG-GUT7090', 'even_MAG-GUT7102', 'even_MAG-GUT7118', 'even_MAG-GUT7121', 'even_MAG-GUT7125', 'even_MAG-GUT71577', 'even_MAG-GUT7175', 'even_MAG-GUT71751', 'even_MAG-GUT7213', 'even_MAG-GUT7214', 'even_MAG-GUT7216', 'even_MAG-GUT7222', 'even_MAG-GUT7253', 'even_MAG-GUT7278', 'even_MAG-GUT7291', 'even_MAG-GUT73376', 'even_MAG-GUT73749', 'even_MAG-GUT73804', 'even_MAG-GUT73847', 'even_MAG-GUT73862', 'even_MAG-GUT74183', 'even_MAG-GUT74662', 'even_MAG-GUT74889', 'even_MAG-GUT74895', 'even_MAG-GUT76377', 'even_MAG-GUT76426', 'even_MAG-GUT76486', 'even_MAG-GUT76518', 'even_MAG-GUT76530', 'even_MAG-GUT7733', 'even_MAG-GUT77471', 'even_MAG-GUT77576', 'even_MAG-GUT77590', 'even_MAG-GUT77597', 'even_MAG-GUT77615', 'even_MAG-GUT77633', 'even_MAG-GUT77900', 'even_MAG-GUT77956', 'even_MAG-GUT78278', 'even_MAG-GUT78295', 'even_MAG-GUT78358', 'even_MAG-GUT78410', 'even_MAG-GUT78413', 'even_MAG-GUT78579', 'even_MAG-GUT78923', 'even_MAG-GUT79180', 'even_MAG-GUT7981', 'even_MAG-GUT80819', 'even_MAG-GUT81671', 'even_MAG-GUT82176', 'even_MAG-GUT82203', 'even_MAG-GUT8281', 'even_MAG-GUT83501', 'even_MAG-GUT83507', 'even_MAG-GUT83922', 'even_MAG-GUT8428', 'even_MAG-GUT84696', 'even_MAG-GUT84793', 'even_MAG-GUT85136', 'even_MAG-GUT8521', 'even_MAG-GUT85568', 'even_MAG-GUT85881', 'even_MAG-GUT85906', 'even_MAG-GUT85926', 'even_MAG-GUT86439', 'even_MAG-GUT86727', 'even_MAG-GUT89162', 'even_MAG-GUT89246', 'even_MAG-GUT89291', 'even_MAG-GUT89323', 'even_MAG-GUT89608', 'even_MAG-GUT89784', 'even_MAG-GUT89815', 'even_MAG-GUT89852', 'even_MAG-GUT90020', 'even_MAG-GUT90054', 'even_MAG-GUT90190', 'even_MAG-GUT90362', 'even_MAG-GUT90441', 'even_MAG-GUT90614', 'even_MAG-GUT90671', 'even_MAG-GUT90675', 'even_MAG-GUT90682', 'even_MAG-GUT90730', 'even_MAG-GUT90775', 'even_MAG-GUT9085', 'even_MAG-GUT9090', 'even_MAG-GUT90941', 'even_MAG-GUT90947', 'even_MAG-GUT90963', 'even_MAG-GUT90995', 'even_MAG-GUT91014', 'even_MAG-GUT91192', 'even_MAG-GUT91196', 'even_MAG-GUT91251', 'even_MAG-GUT91262', 'even_MAG-GUT91264', 'even_MAG-GUT91267', 'even_MAG-GUT91272', 'even_MAG-GUT91297', 'even_MAG-GUT91303', 'even_MAG-GUT91320', 'even_MAG-GUT91328', 'even_MAG-GUT91330', 'even_MAG-GUT91385', 'even_MAG-GUT91468', 'even_MAG-GUT91470', 'even_MAG-GUT91486', 'even_MAG-GUT91490', 'even_MAG-GUT91491', 'even_MAG-GUT91492', 'even_MAG-GUT91496', 'even_MAG-GUT91520', 'even_MAG-GUT91536', 'even_MAG-GUT91546', 'even_MAG-GUT91566', 'even_MAG-GUT91568', 'even_MAG-GUT91702', 'even_MAG-GUT91712', 'even_MAG-GUT91717', 'even_MAG-GUT91736', 'even_MAG-GUT91762', 'even_MAG-GUT91779', 'even_MAG-GUT91815', 'even_MAG-GUT91818', 'even_MAG-GUT91821', 'even_MAG-GUT91823', 'even_MAG-GUT91833', 'even_MAG-GUT91860', 'even_MAG-GUT91882', 'even_MAG-GUT91886', 'even_MAG-GUT91898', 'even_MAG-GUT91911', 'even_MAG-GUT91912', 'even_MAG-GUT91923', 'even_MAG-GUT91926', 'even_MAG-GUT91932', 'even_MAG-GUT91941', 'even_MAG-GUT91943', 'even_MAG-GUT91954', 'even_MAG-GUT91960', 'even_MAG-GUT92006', 'even_MAG-GUT92066', 'even_MAG-GUT92111', 'even_MAG-GUT940', 'even_MAG-GUT945', 'even_MAG-GUT9681', 'even_MAG-GUT9766', 'even_MAG-GUT984', 'even_MAG-GUT25847', 'even_MAG-GUT32882', 'even_MAG-GUT36916', 'even_MAG-GUT38145', 'even_MAG-GUT41020', 'even_MAG-GUT42710', 'even_MAG-GUT58949', 'even_MAG-GUT59149', 'even_MAG-GUT74962', 'even_MAG-GUT81578', 'even_MAG-GUT89102', 'even_MAG-GUT89309', 'even_MAG-GUT89335', 'even_MAG-GUT89577', 'even_MAG-GUT89735']
precision2, recall2, incorrect_rate2, partial_recall2, rej_stats2 = calc_stats(path2, ranks2, ignore_indices=ignore_indices2)
print("precision is:", precision2, "recall is:", recall2, "incorrect rate is:", incorrect_rate2, "partial recall is:", partial_recall2)
for r in rej_stats2:
    print(rej_stats2[r], "rejects at ", r)
print("total rejection rate is:", sum(rej_stats2.values()))





            
                    



