#!/bin/sh
i=0  
while true 
pre_proc_num=0
do  
    echo "iteration ${i}"
    cur_proc_num=`echo $(screen -ls)|grep -Po "[[:digit:]]+ *(?=Socket)"`
    if [ $cur_proc_num -lt $pre_proc_num ] || [ $i == 0 ]; then
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
        python3 outputs-r202/group_pred.py phylum
        python3 outputs-r202/group_pred.py class
        python3 outputs-r202/group_pred.py order
        python3 outputs-r202/group_pred.py family
        python3 outputs-r202/group_pred.py genus
        python3 outputs-HGR-r202/group_pred_HGR.py class
        python3 outputs-HGR-r202/group_pred_HGR.py order
        python3 outputs-HGR-r202/group_pred_HGR.py family
        python3 outputs-HGR-r202/group_pred_HGR.py genus
        echo "==== begin checking_missing_exec ====" 
        python3 checking_missing_exec.py True
    else
            echo "No processes finished."
    fi

    pre_proc_num=$cur_proc_num
    echo "==== begin sleep 5 minutes at $(date)===="
    sleep 300
    i=$((i+1))  
done