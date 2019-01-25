#!/bin/bash
# create training lmdb:
mkdir -p /code/nonlocal/data/lmdb
mkdir -p /code/nonlocal/data/lmdb/DIVA_lmdb_multicrop
python ../kinetics/create_video_lmdb.py --dataset_dir /code/nonlocal/data/lmdb/DIVA_lmdb_multicrop/train  --list_file /data/divaTrainTestList20/trainlist01_video_shuffle_rep.txt

# create val lmdb:
# python ../kinetics/create_video_lmdb.py --dataset_dir ../../data/lmdb/DIVA_lmdb_multicrop/val  --list_file /data/weik/DIVA/divaTrainTestList20/vallist.txt
