import os
import glob
import argparse

data_folders = '/home/users/dawei.yang/data/source_eye_data/'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-root_dir', help='root dir', default=data_folders)
    parser.add_argument('-dir_type', help='[o]"a_open|glass_open|a_close|glass_close"',
                        default='a_open|glass_open|a_close|glass_close')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    sub_dirs = os.walk(args.root_dir)
    dir_types = args.dir_type.split('|')
    dir_types_num = {}
    sub_dir_types_num = {}
    for sub_dir_files in sub_dirs:
        sub_dir = sub_dir_files[0]
        if sub_dir.split(os.sep)[-1] in dir_types:
            dir_type = sub_dir.split(os.sep)[-1]
            if dir_type not in dir_types_num:
                dir_types_num[dir_type] = 0
            # count the number of files
            num = len(glob.glob(sub_dir + '/*'))
            tmp_path = os.sep.join(sub_dir.split(os.sep)[6:-1])
            if tmp_path not in sub_dir_types_num:
                sub_dir_types_num[str(tmp_path)] = {}
                sub_dir_types_num[str(tmp_path)][dir_type] = num
            else:
                sub_dir_types_num[str(tmp_path)][dir_type] = num
            dir_types_num[dir_type] += num
    key_lst = sorted(sub_dir_types_num.keys())
    #     longest = max(len(line.strip()) for line in key_lst)
    #     print longest
    print ("|  %-4s  | %-55s | %-10s | %-10s | %-10s | %-11s |    " % (
        "ID", "video_name", "a_open", "a_close", "glass_open", "glass_close"))
    for r in key_lst:
        if 'a_open' not in sub_dir_types_num[r]:
            a_open = 0
        else:
            a_open = sub_dir_types_num[r]['a_open']
        if 'a_close' not in sub_dir_types_num[r]:
            a_close = 0
        else:
            a_close = sub_dir_types_num[r]['a_close']
        if 'glass_open' not in sub_dir_types_num[r]:
            glass_open = 0
        else:
            glass_open = sub_dir_types_num[r]['glass_open']
        if 'glass_close' not in sub_dir_types_num[r]:
            glass_close = 0
        else:
            glass_close = sub_dir_types_num[r]['glass_close']
        print ("|  %-4d  | %-55s | %-10d | %-10d | %-10d | %-11d |    " % (
            key_lst.index(r), str(r), a_open, a_close, glass_open, glass_close))
        #         print str(r) + ':' + str(sub_dir_types_num[r])
    print ("|  %-4s  | %-55s | %-10d | %-10d | %-10d | %-11d |    " % (
        "xx", "sum up", dir_types_num['a_open'], dir_types_num['a_close'], dir_types_num['glass_open'],
        dir_types_num['glass_close']))
