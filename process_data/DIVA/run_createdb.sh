#!/usr/bin/env bash

# create training lmdb:
# each row in lmdb: video_file_name, label
mkdir -p ../../data/lmdb
mkdir -p ../../data/lmdb/DIVA_lmdb_multicrop
python ../kinetics/create_video_lmdb.py --dataset_dir ../../data/lmdb/DIVA_lmdb_multicrop/train  --list_file /data/weik/DIVA/divaTrainTestList20/trainlist_shuffle_rep.txt

# create val lmdb:
# python ../kinetics/create_video_lmdb.py --dataset_dir ../../data/lmdb/DIVA_lmdb_multicrop/val  --list_file /data/weik/DIVA/divaTrainTestList20/vallist.txt