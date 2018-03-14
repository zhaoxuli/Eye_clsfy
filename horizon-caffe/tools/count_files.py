### python ~/work/MyPython/count_files.py -root_dir=./
### python ~/work/MyPython/count_files.py -root_dir=./ -dir_type="a_close|class_close"

import os
import glob
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-root_dir', help='root dir')
    parser.add_argument('-dir_type', help='[o]a_open|glass_open|a_close|glass_close',
                        default='a_open|glass_open|a_close|glass_close')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    sub_dirs = os.walk(args.root_dir)
    dir_types = args.dir_type.split('|')
    total_num = 0
    for sub_dir_files in sub_dirs:
        sub_dir = sub_dir_files[0]

        ### Check if sub_dir is matched with anyone in dir_type
        for dir_type in dir_types:
            if dir_type in sub_dir:
                ### count the number of files in this sub_dir
                num = len(glob.glob(sub_dir+'/*'))
                total_num += num
                print sub_dir, num

                break
    print total_num
