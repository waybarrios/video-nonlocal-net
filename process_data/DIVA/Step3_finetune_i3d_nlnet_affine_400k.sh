#!/bin/bash

CHECKPOINT_DIR=../../data/checkpoints/run_i3d_nlnet_affine_400k
mkdir ${CHECKPOINT_DIR}

python ../../tools/train_net_video.py \
--config_file ./configs/DBG_kinetics_resnet_8gpu_c2d_nonlocal_affine_400k.yaml \
TRAIN.PARAMS_FILE /model/pretrained_model/output/nonlocal_32x4_diva.pkl \
VIDEO_DECODER_THREADS 2 \
NONLOCAL.CONV3_NONLOCAL True \
NONLOCAL.CONV4_NONLOCAL True \
MODEL.VIDEO_ARC_CHOICE 2 \
TRAIN.DROPOUT_RATE 0.5 \
CHECKPOINT.DIR ${CHECKPOINT_DIR} \
DATADIR ../data/lmdb/kinetics_lmdb_multicrop/ \
FILENAME_GT ../process_data/kinetics/vallist.txt \
2>&1 | tee ${CHECKPOINT_DIR}/log.txt