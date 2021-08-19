#!/bin/sh

: '
Script for grouping test sequences, and calling check_missing_pred 
periodically
'

i=0  
pre_proc_num=0
while true
do  
    echo "iteration ${i}"
    cur_proc_num=`echo $(screen -ls)|grep -Po "[[:digit:]]+ *(?=Socket)"`
    echo "cur_proc_num is: $cur_proc_num"
    echo "pre_proc_num is: $pre_proc_num"
    if [ $cur_proc_num -ne $pre_proc_num ] || [ $i == 0 ]; then
        echo "==== git commit ===="
        cd ~/MLDSP
        git add .
        git commit -m "updated outputs"
        git push
        cd ~/BlindKameris-new
        git add .
        git commit -m "updated outputs"
        git push
        echo "==== begin group_pred ===="
        # python3 outputs-r202/group_pred.py phylum
        python3 outputs-r202/group_pred.py class
        python3 outputs-r202/group_pred.py order
        python3 outputs-r202/group_pred.py family
        python3 outputs-r202/group_pred.py genus
        python3 outputs-HGR-r202/group_pred_HGR.py class
        python3 outputs-HGR-r202/group_pred_HGR.py order
        python3 outputs-HGR-r202/group_pred_HGR.py family
        python3 outputs-HGR-r202/group_pred_HGR.py genus
        echo "==== begin check_missing_exec ====" 
        python3 check_missing_exec.py True
    else
        echo "No processes finished."
    fi

    pre_proc_num=$cur_proc_num
    echo "==== begin sleep 5 minutes at $(date)===="
    sleep 300
    i=$((i+1))  
done