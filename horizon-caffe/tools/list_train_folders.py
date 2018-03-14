import os
import glob
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-root_dir', help='root dir')
    parser.add_argument('-dir_type', help='[o]"a_open|glass_open|a_close|glass_close"', default='a_open|glass_open|a_close|glass_close')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    sub_dirs = os.walk(args.root_dir)
    dir_types = args.dir_type.split('|')
    for sub_dir_files in sub_dirs:
        sub_dir = sub_dir_files[0]
        if sub_dir.split(os.sep)[-1] in dir_types:
            print sub_dir