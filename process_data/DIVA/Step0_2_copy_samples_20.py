import os
import pickle as pl
import json

def copy_samples_20(file_list, src_dir, dst_dir, label_id_list):

    count = 0
    for video_name, video_info in file_list.items():
        src_path = os.path.join(src_dir, video_name)

        start_frame = video_info["start_frame"]
        event_begin = video_info["event_begin"]
        event_end = video_info["event_end"]

        actv_name = video_info['props_label']
        if actv_name not in label_id_list:
            actv_name = 'Other'

        if not os.path.exists(os.path.join(dst_dir, actv_name)):
            os.makedirs(os.path.join(dst_dir, actv_name))

        dst_path = os.path.join(os.path.join(dst_dir, actv_name), actv_name + '_' + video_name.split('/')[-1])
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        begin_t = event_begin - start_frame + 1
        frame_count = 0
        for image_idx in range(event_begin-start_frame+1, event_end - start_frame+1):
            img_src = os.path.join(src_path, 'image_{:05d}.jpg'.format(image_idx))
            img_dst = os.path.join(dst_path, 'image_{:05d}.jpg'.format(image_idx - begin_t + 1))
            if os.path.exists(img_src):
                cmd = 'cp -r {0} {1}'.format(img_src, img_dst)
                os.system(cmd)
                frame_count = frame_count + 1

        with open(os.path.join(dst_path, 'n_frames'), 'w') as dst_file:
            dst_file.write(str(frame_count))

        count = count + 1
        print(count)


def get_file_list(split):
    annotation_path = '/data/weik/DIVA/SharedData/instance_list/export_gt_cls_baseline/{0}/'.format(split)

    phases = ['train', 'test']
    file_list = {}
    for phase in phases:
        input_files = []
        input_files_info = {}

        with open(os.path.join(annotation_path, phase + '.json'), 'rb') as f:
            actv_list = json.load(f)

        for idx, sample in enumerate(actv_list):
            video_name = sample['video_name']
            props_name = sample['props_name']
            props_type = sample['props_type']
            file_path = [video_name[8:12], video_name]

            video_name = os.path.join(os.path.join(os.path.join(file_path[0]), file_path[1]), props_name)
            input_files.append(video_name)
            input_files_info[video_name] = actv_list[idx]

        file_list[phase] = input_files_info

    return file_list


if __name__ == "__main__":

    split = 'split1'
    DIVASamples_dir = '/data/weik/DIVA/SharedDataProposals/'
    save_dir = '/data/weik/DIVA/JPG20'
    if os.path.exists(save_dir):
        cmd = 'rm -rf {0}'.format(save_dir)
        os.system(cmd)


    ################################################################
    ## load label names
    ## load label names
    label_id_file = '/data/weik/DIVA/SharedData/label_list.pkl'
    fr = open(label_id_file, 'rb')
    label_id_list = pl.load(fr)
    fr.close()
    label_id_list.insert(0, 'Other')


    ################################################################
    # get info
    file_list = get_file_list(split)
    train_file_list = file_list['train']
    test_file_list = file_list['test']

    ################################################################
    # create soft links
    copy_samples_20(train_file_list, DIVASamples_dir, save_dir, label_id_list)
    copy_samples_20(test_file_list, DIVASamples_dir, save_dir, label_id_list)


