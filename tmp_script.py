# f__Turicibacteraceae
# f__UBA11471
# f__UBA660
# f__UBA932
# g__Alistipes
# g__Alistipes_A
# g__Amedibacillus
# g__Amedibacterium
# g__Anaerotignum
# g__Bacteroides_F
# g__Barnesiella
# g__Blautia
# g__Blautia_A
# g__Bulleidia
# g__CAG-1031
# g__CAG-194
# g__CAG-279
# g__CAG-288
# g__CAG-302
# g__CAG-307
# g__CAG-313
# g__CAG-345
# g__CAG-485
# g__CAG-590
# g__CAG-605
# g__CAG-631
# g__CAG-791
# g__CAG-81
# g__CAG-873
# g__CAG-882
# g__CAG-988
# g__Clostridium_AP
# g__Dorea_A
# g__Enterococcus
# g__Enterococcus_B
# g__Enterococcus_D
# g__Erysipelatoclostridium
# g__Eubacterium_F
# g__Eubacterium_G
# g__Faecalibacillus
# g__Faecalimonas
# g__Lachnospira
# g__Lactobacillus
# g__Ligilactobacillus
# g__Limosilactobacillus
# g__Mediterraneibacter
# g__Phocaeicola
# g__Porphyromonas
# g__Prevotella
# g__Prevotellamassilia
# g__RC9
# g__Schaedlerella
# g__Staphylococcus
# g__Streptococcus
# g__TF01-11
# g__Tidjanibacter
# g__Turicibacter
# g__UBA11471
# g__UBA4855
# g__UBA4951
# g__UBA7057
# g__UBA733
# g__UBA7642
# g__UBA9502
# g__UMGS75
# o__Acholeplasmatales
# o__Bacteroidales
# o__Erysipelotrichales
# o__Haloplasmatales_A
# o__Lactobacillales
# o__ML615J-28
# o__RF39
# o__RFN20
# o__Staphylococcales

import os
import sys
import subprocess
import time

classes = ["f__Turicibacteraceae",
"f__UBA11471",
"f__UBA660",
"f__UBA932",
"g__Alistipes"]

for c in classes:
    os.system('screen -dm bash -c "cd ~/MLDSP; bash phase_HGR_test.sh '+c + '"')
    print('enter screen -dm bash -c "cd ~/MLDSP; bash phase_HGR_test.sh '+c + '"')
