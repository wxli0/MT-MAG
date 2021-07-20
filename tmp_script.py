import os
import sys
import subprocess
import time

classes = [
"f__UBA3663",
"g__UBA7741",
"f__RUG033",
"g__UBA1756",
"g__Catonella",
"g__RUG727",
"g__RUG842",
"g__Intestinibaculum",
"g__Kandleria",
"g__RUG131",
"g__CAG-964",
"g__Sharpea",
"f__Mycoplasmoidaceae",
"g__UBA3633",
"g__CAG-103",
"g__RUG159",
"g__Malacoplasma_A",
"g__RUG591",
"g__UBA2730",
"f__UMGS124",
"g__RUG705",
"g__UBA4293",
"g__RUG762",
"g__WRAD01",
"g__RUG572",
"g__UBA629",
"c__Lentisphaeria",
"g__UBA2918",
"g__RUG210",
"g__UBA2912",
"g__Olegusella",
"f__UBA1390",
"f__UBA1407",
"g__RUG306",
"g__RUG440",
"g__UBA3663",
"g__CAG-390",
"g__UBA2882",
"g__Alloprevotella",
"f__Bifidobacteriaceae",
"f__UBA1067",
"g__Catenibacterium",
"f__Streptococcaceae",
"g__RUG592",
"g__Lactococcus",
"g__CAG-180",
"g__UBA1217",
"g__UBA1367",
"g__UBA3207",
"g__Weimerbacter",
"o__UBA1407",
"f__WCHB1-69",
"g__CAG-1000",
"f__P3",
"g__UBA6398",
"o__ML615J-28",
"g__UBA2450",
"g__UBA3839",
"f__F082",
"g__UBA3789",
"g__Olsenella",
"f__UBA932",
"g__UBA1232",
"f__Erysipelatoclostridiaceae",
"g__Faecalimonas",
"g__UBA4285",
"f__Atopobiaceae",
"g__CAG-590",
"g__Bulleidia",
"g__AC2028",
"g__F23-D06",
"g__CAG-603",
"g__UBA1777",
"g__Ruminococcus_D",
"g__UBA6382",
"g__UBA1067",
"o__RFP12",
"g__CAG-83",
"f__CAG-826",
"g__UBA4951",
"g__NK4A136",
"f__Muribaculaceae",
"f__Paludibacteraceae",
"f__UBA1242",
"g__Eubacterium_F",
"g__CAG-110",
"g__CAG-127",
"g__UBA1179",
"g__Eubacterium_H",
"f__Desulfovibrionaceae",
"g__Agathobacter",
"g__UBA4334",
"g__Lachnospira",
"g__UBA2856",
"f__CAG-272",
"g__Bacillus",
"g__Oribacterium",
"g__UBA1066",
"g__UBA1213",
"g__Butyrivibrio",
"f__Bacteroidaceae",
"g__Eubacterium_Q",
"g__CAG-791",
"root",
"g__F082",
"f__Erysipelotrichaceae",
"g__Blautia_A",
"g__UBA1711",
"o__Erysipelotrichales",
"g__CAG-485",
"g__UBA4372",
"o__RFN20",
"f__Oscillospiraceae",
"c__Kiritimatiellae",
"o__Desulfovibrionales",
"c__Desulfovibrionia",
"g__Ruminococcus_E",
"f__Ruminococcaceae",
"g__Sodaliphilus",
"f__Acutalibacteraceae",
"o__Lachnospirales",
"o__Bacillales",
"o__Mycoplasmatales",
"o__RF39",
"o__Actinomycetales",
"g__RF16",
"p__Firmicutes",
"f__UBA660",
"c__Coriobacteriia",
"g__Bifidobacterium",
"o__Coriobacteriales",
"g__RC9",
"c__Bacilli",
"o__Bacteroidales",
"c__Actinomycetia",
"c__Bacteroidia",
"o__Lactobacillales",
"f__Lachnospiraceae",
"g__Prevotella"]

for c in classes:
    os.system('screen -dm bash -c "cd ~/MLDSP; bash phase_test.sh '+c + '"')
    print('enter screen -dm bash -c "cd ~/MLDSP; bash phase_test.sh '+c + '"')
