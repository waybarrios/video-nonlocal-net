# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import argparse
import fnmatch
import glob
import json
import os
import shutil
import subprocess
import uuid
import cv2

import glob
from joblib import delayed
from joblib import Parallel

folder_path = '/data/weik/DIVA/JPG20'
output_path = '/data/weik/DIVA/JPG20_256'

def downscale_clip_wrapper(row):

    nameset  = row.split(' ')
    videoname = nameset[0]

    inpath = folder_path + '/' + videoname
    outpath = output_path + '/' + videoname
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    image_list = glob.glob("{0}/*.jpg".format(inpath))
    for image_name in image_list:
        inname = image_name.split('/')[-1]
        img_src = cv2.imread(image_name)
        img_size_src = img_src.shape
        height = img_size_src[0]
        width = img_size_src[1]
        nchannel = img_size_src[2]
        new_width = int(256.0/float(height) * float(width))
        img_resized = cv2.resize(img_src, (256, new_width))
        cv2.imwrite(os.path.join(outpath, inname), img_resized)

    nframe_src = os.path.join(inpath, 'n_frames')
    nframe_dst = os.path.join(outpath, 'n_frames')
    if os.path.exists(nframe_src):
        cmd = 'cp -r {0} {1}'.format(nframe_src, nframe_dst)
        os.system(cmd)
    else:
        print(videoname + ": error")


if __name__ == "__main__":

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_src = '/data/weik/DIVA/divaTrainTestList20/trainlist01.txt'
    file_list = []
    f = open(file_src, 'r')
    for line in f:
        rows = line.split()
        fname = rows[0]
        file_list.append(fname)
    f.close()
    status_lst = Parallel(n_jobs=16)(delayed(downscale_clip_wrapper)(row) for row in file_list)

    file_src = '/data/weik/DIVA/divaTrainTestList20/vallist01.txt'
    file_list = []
    f = open(file_src, 'r')
    for line in f:
        rows = line.split()
        fname = rows[0]
        file_list.append(fname)
    f.close()
    status_lst = Parallel(n_jobs=16)(delayed(downscale_clip_wrapper)(row) for row in file_list)
