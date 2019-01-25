################################################################
# the frame name starts from 1
# with format %06d.png
################################################################

import cv2
import os
import glob
import subprocess

import sys
import subprocess
import json
import pickle as pl

print(cv2.__version__)

### for validation
annotation_path = '/data/weik/DIVA/SharedData/instance_list/export_gt_cls_baseline/'
video_path = '/data/weik/DIVA/SharedData/trajectory_images/'

phases = ['train', 'test']

save_path = "/data/weik/DIVA/SharedDataProposals"
save_path_event = "/data/weik/DIVA/SharedDataProposalsEvent"


for phase in phases:
    with open(os.path.join(annotation_path, 'split1', phase + '.json'), 'r') as f:
        annotation_file_lists = json.load(f)
    
    count = 0
    for annotation_file_idx, annotation_info in enumerate(annotation_file_lists):
        props_type = annotation_info['props_type']
        props_name = annotation_info["props_name"]
        props_label = annotation_info['props_label']
        start_frame = annotation_info["start_frame"]
        end_frame = annotation_info["end_frame"]
        event_begin = annotation_info["event_begin"]
        event_end = annotation_info["event_end"]
        video_name = annotation_info["video_name"]

        if not os.path.exists(os.path.join(video_path, props_type, props_name, 'video.mp4')):
            print('there is no event proposal in ' + props_name)
            continue

        print("Extracting ---> {0}".format(video_name))
        file_path = [video_name[8:12], video_name]
        if os.path.exists(os.path.join(save_path_event, file_path[0], file_path[1], props_name,'n_frames')):
            print("Extracting ---> {0}".format(video_name))
            continue

        read_path = os.path.join(video_path, props_type, props_name, 'video.mp4')
        store_path = os.path.join(save_path, file_path[0], file_path[1], props_name)
        if not os.path.exists(store_path):
            os.makedirs(store_path)
        cmd = 'ffmpeg -loglevel 0 -i \"{}\"  \"{}/image_%05d.jpg\"'.format(read_path, store_path)
        print(cmd)
        subprocess.call(cmd, shell=True)

        frame_count = 0
        for fn in os.listdir(store_path):
            frame_count = frame_count + 1

        with open(os.path.join(store_path, 'n_frames'), 'w') as dst_file:
            dst_file.write(str(frame_count))

        begin_t = event_begin - start_frame + 1
        src_path = os.path.join(save_path, file_path[0], file_path[1], props_name)
        dst_path = os.path.join(save_path_event, file_path[0], file_path[1], props_name)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        frame_count = 0
        for image_idx in range(event_begin - start_frame + 1, event_end - start_frame + 1):
            img_src = os.path.join(src_path, 'image_{:05d}.jpg'.format(image_idx))
            img_dst = os.path.join(dst_path, 'image_{:05d}.jpg'.format(image_idx - begin_t + 1))
            if os.path.exists(img_src):
                cmd = 'cp -r {0} {1}'.format(img_src, img_dst)
                os.system(cmd)
                frame_count = frame_count + 1

        with open(os.path.join(dst_path, 'n_frames'), 'w') as dst_file:
            dst_file.write(str(frame_count))

        count = count+1
        print(count)