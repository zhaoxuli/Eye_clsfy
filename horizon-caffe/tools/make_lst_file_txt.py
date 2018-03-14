#-*- coding: UTF-8 -*-

# Read pictures from 5 pre-categorized folders respecitively, save the image name and its eye status into
# a txt file. Below are 5 types of pre-categorized folders:
# 'open', 'closed', 'uncertain', 'occlusion', 'invisible'

# usage: python sumUp_eye.py

import os
import glob
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    ### root_dir = '/media/psf/TF128-OV/uhome/dms20170418_1801303733/'
    parser.add_argument('-root_dir', type=str, help='[o]', default='')
    parser.add_argument('-folder_list', type=str)
    #parser.add_argument('-pic_ext', type=str, default='.png')
    args = parser.parse_args()

    if args.root_dir != '' and args.root_dir[-1] != os.sep:
        args.root_dir += os.sep
    return args


def skip_comments_and_blank(file, cm='#'):
    lines = list()
    for line in file:
        if not line.strip().startswith(cm) and not line.isspace():
            lines.append(line)
    return lines


if __name__ == '__main__':
    args = parse_args()

    lines = skip_comments_and_blank(open(args.folder_list))
    lines = map(lambda x: x.strip(), lines)
    folder_list = map(lambda x: x.split(), lines)
    print folder_list

    i = 0
    for folder, num in folder_list:
        if folder[-1] != os.sep:
            folder += os.sep
        # print folder, num
        img_names = glob.glob(args.root_dir + folder + '/*.png')
        for img_name in img_names:
            i += 1
            print ('%d\t%d\t%s' % (i, int(num), img_name))
