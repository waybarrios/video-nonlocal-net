import os

if __name__ == '__main__':
    csv_dir_path = '/data/weik/DIVA/divaTrainTestList20'

    for idx in range(1,5):
        for phase in ['train', 'val', 'test']:
            csv_path = os.path.join(csv_dir_path, '{}list0{}.txt'.format(phase, idx))

            file_src = csv_path
            file_dst = os.path.join(csv_dir_path, '{}list0{}_video.txt'.format(phase, idx))
            file_list = []
            f = open(file_src, 'r')
            f_out = open(file_dst, 'w')
            for line in f:
                rows = line.split()
                fname = rows[0] + '/video.mp4'
                if phase is not 'test':
                    label = rows[1]
                    f_out.write('{} {}\n'.format(fname, label))
                else:
                    f_out.write('{}\n'.format(fname))

            f.close()
            f_out.close()