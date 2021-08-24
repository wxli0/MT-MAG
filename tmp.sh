#!/bin/bash
ind=0
count=`ls -l /mnt/sda/DeepMicrobes-data/labeled_genome-r202/p__Verrucomicrobiota|wc -l`
if [ $count == 4 ]; then
	ind=1
	echo "enter here"
fi
echo ${ind}
