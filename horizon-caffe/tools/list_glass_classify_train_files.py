#-*- coding: UTF-8 -*-

# Read pictures from 5 pre-categorized folders respecitively, save the image name and its eye status into
# a txt file. Below are 5 types of pre-categorized folders:
# 'open', 'closed', 'uncertain', 'occlusion', 'invisible'

# usage: python sumUp_eye.py

import os
import glob
import argparse

dir_types = {'a_close':0, 'a_open':0, 'glass_close':1, 'glass_open':1}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-root_dir', type=str, help='[o]', default='')
    #parser.add_argument('pic_class', type=int, help='which class does the pictures in the folder belongs to')
    parser.add_argument('folder', type=str)
    parser.add_argument('-recursive', type=str, default='0')

    args = parser.parse_args()

    if args.root_dir != '' and args.root_dir[-1] != os.sep:
        args.root_dir += os.sep

    if args.folder[-1] != os.sep:
        args.folder += os.sep
    return args


if __name__ == '__main__':
    args = parse_args()

    if args.recursive == '1':
        sub_dirs = os.walk(args.root_dir+args.folder)
        for sub_dir_files in sub_dirs:
            sub_dir = sub_dir_files[0]
            dir_type = sub_dir.split(os.sep)[-1]
            if dir_type in dir_types:
                img_names = glob.glob(sub_dir + '/*.png')
                for img_name in img_names:
                    print img_name, dir_types[dir_type]
    else:
        # last_folder = 'a_close' in '/home/20170419_JOC/17PM/1794234160/a_close'
        last_folder = args.folder.split(os.sep)[-2]
        img_names = glob.glob(args.root_dir + args.folder + '*.png')
        for img_name in img_names:
           print img_name, dir_types[last_folder]
