### python ~/work/MyPython/rename_files.py -src_dir=./1797900845/a_open

import os
import glob
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-src_dir', help='source dir')
    parser.add_argument('-preview', help='only print the modification, but do not do the change', default=False)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    files = glob.glob(args.src_dir + os.path.sep + '*')
    for f in files:
        ## remove path
        f = f.split(os.path.sep)[-1]

        if f.startswith('right') or f.startswith('left'):
            continue
        ## "9950_0_21639.png" => 9950 ,right, 21639
        conf, rl, img = f.split('_')
        if rl == '0':
            fnew = 'right_' + img
        else:
            fnew = 'left_' + img

        fold = args.src_dir + os.path.sep + f
        fnew = args.src_dir + os.path.sep + fnew
        print fold, '=>', fnew
        if not args.preview:
            os.rename(fold, fnew)
