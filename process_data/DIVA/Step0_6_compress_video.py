import cv2
import os
import glob

import sys
import subprocess
import json
import pickle as pl
from joblib import delayed
from joblib import Parallel


folder_path = '/data/weik/DIVA/JPG20_256'
output_path = '/data/weik/DIVA/JPG20_256_video'
if not os.path.exists(output_path):
    os.makedirs(output_path)

def compress_video(video_name):
    store_path = os.path.join(output_path, video_name)
    if not os.path.exists(store_path):
        os.makedirs(store_path)
    read_path = os.path.join(folder_path, video_name)
    cmd = 'ffmpeg -f image2 -i \"{}/image_%05d.jpg\" -y \"{}/video.mp4\"'.format(read_path, store_path)
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    csv_dir_path = '/data/weik/DIVA/divaTrainTestList20'

    train_csv_path = os.path.join(csv_dir_path, 'trainlist01.txt')
    val_csv_path = os.path.join(csv_dir_path, 'testlist01.txt')

    file_src = train_csv_path
    file_list = []
    f = open(file_src, 'r')
    for line in f:
        rows = line.split()
        fname = rows[0]
        file_list.append(fname)
    f.close()
    status_lst = Parallel(n_jobs=16)(delayed(compress_video)(row) for row in file_list)


    file_src = val_csv_path
    file_list = []
    f = open(file_src, 'r')
    for line in f:
        rows = line.split()
        fname = rows[0]
        file_list.append(fname)
    f.close()
    status_lst = Parallel(n_jobs=16)(delayed(compress_video)(row) for row in file_list)