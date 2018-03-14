#! /usr/bin/env python

import os
import glob
import argparse


predict_txt = '/home/fenghan/work/tools_script/file_lists/predict_folders.txt'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-folder_lst', help='folder lst', default=predict_txt)
    parser.add_argument('-replace', help='replace prefix', default=False)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    with open(args.folder_lst, 'r') as folders:
        l = folders.readlines()
        for i in l:
            imgs = glob.glob(i.strip() + os.sep + '*')
            for f in imgs:
                if args.replace:
                    f = f.replace('/home/fenghan/Videos', '/home/users/dawei.yang/data/source_eye_data')
                print f
