import os
import pickle as pl
import json

splits = ['split1', 'split2', 'split3', 'split4']
list_dir = '/data/weik/DIVA/divaTrainTestList20'
if not os.path.exists(list_dir):
    os.makedirs(list_dir)

## load label names
label_id_file = '/data/weik/DIVA/SharedData/label_list.pkl'
fr = open(label_id_file, 'rb')
label_id_list = pl.load(fr)
fr.close()
label_id_list.insert(0, 'Other')


# read the sample list of train/test
input_files = []
input_files_info = {}

video_dir = '/data/weik/DIVA/JPG20'


def create_list(idx, phase, file_list):
    with open(os.path.join(list_dir, '{0}list{1:02}.txt'.format(phase, idx)), 'w') as list_file:
        for video_name, video_info in file_list.items():

            actv_name = video_info['props_label']
            if actv_name not in label_id_list:
                actv_name = 'Other'

            parts = [video_name.split('/')[-2], video_name.split('/')[-1]]
            sample_path = os.path.join(actv_name, actv_name + '_' + video_name.split('/')[-1])

            if phase == 'train' or phase == 'val':
                list_file.write('{} {}\n'.format(sample_path, label_id_list.index(actv_name) + 1))
            elif phase == 'test':
                list_file.write('{}\n'.format(sample_path))

    list_file.close()

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


if __name__=='__main__':

    #################################################################################
    # create classInd file
    # classInd file
    with open(os.path.join(list_dir, 'classInd.txt'), 'w') as classind_file:
        for idx, category_name in enumerate(label_id_list):
            classind_file.write('{0:d} {1}\n'.format(idx+1, category_name))
    classind_file.close()


    ################################################################
    # create training and testing list
    # train list
    for idx, split in enumerate(splits):
        ################################################################
        # get info

        file_list = get_file_list(split)
        train_file_list = file_list['train']
        test_file_list = file_list['test']

        create_list(idx + 1, 'train', train_file_list)
        create_list(idx + 1, 'val', test_file_list)
        create_list(idx + 1, 'test', test_file_list)







