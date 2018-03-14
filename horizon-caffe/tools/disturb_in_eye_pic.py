# -*- coding: UTF-8 -*-

import os
import sys
import glob
import numpy as np
import cv2
import argparse

# if test_ratio = [1, 5], then:
# 1. idx % 10 == [0, 2, 3, 4, 6, 7, 8, 9] saves to 'train folders'
# 2. idx % 10 == [1, 5] saves to 'test folders'
test_ratio = [1, 5]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pic_dir', type=str)
    parser.add_argument('-save_path', type=str)
    parser.add_argument('-disturb_time', type=int, default=10, help='[o]')
    args = parser.parse_args()

    if args.save_path[-1] != os.sep:
        args.save_path += os.sep
    return args


def append_diff_part_path(path_src, path_dst):
    src_list = str(path_src).split(os.sep)
    dst_list = str(path_dst).split(os.sep)
    for path_part in src_list:
        if path_part not in dst_list:
            dst_list.append(path_part)
    return os.sep.join(dst_list)


class B:
    def __init__(self, args, debug=0):
        self.pic_dir = args.pic_dir
        self.save_path = args.save_path
        self.disturb_time = args.disturb_time

        self.cut_scale = '1.8x1.8'
        if debug == 1:
            print 'args:', args

    def get_eye_rect(self, m1, m2, n1, n2, width, height):
        w = width / float(m1)
        ox = (n1 - m1) * w / 2.0
        oy = (n2 - m2) * w / 2.0
        return 0 - ox, 0 - oy, width + ox, height + oy

    def generate_disturb_rect(self, rect, context, img_w, img_h):
        import random
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        x0 = rect[0] + random.random() * w * context
        x1 = rect[2] - random.random() * w * context
        x2 = rect[2] - random.random() * w * context
        x3 = rect[0] + random.random() * w * context
        y0 = rect[1] + random.random() * w * context
        y1 = rect[1] + random.random() * w * context
        y2 = rect[3] - random.random() * w * context
        y3 = rect[3] - random.random() * w * context
        x0 = 0 if x0 < 0 else x0
        x1 = img_w if x1 > img_w else x1
        x2 = 0 if x2 < 0 else x2
        x3 = img_w if x3 > img_w else x3
        y0 = 0 if y0 < 0 else y0
        y1 = 0 if y1 < 0 else y1
        y2 = img_h if y2 > img_h else y2
        y3 = img_h if y3 > img_h else y3
        res = np.zeros((4, 2), dtype="float32")
        res[:, 0] = [x0, x1, x2, x3]
        res[:, 1] = [y0, y1, y2, y3]
        return res

    def process(self):
        # for dir, algo_res_file, video in self.algofile_list:
        dir = self.pic_dir
        print "[Processing]", dir

        src_files = glob.glob(dir + os.path.sep + '*')
        img_idx = 0
        for img_name in src_files:
            img = cv2.imread(img_name)
            height, width, channel = img.shape
            left, top, right, bottom = self.get_eye_rect(2.0, 2.0, 1.8, 1.8, width, height)

            eye_rect = [left, top, right, bottom]

            dst_vertex = np.zeros((4, 2), dtype="float32")
            dst_vertex[:, 0] = [left, right, right, left]  # [left, right, right, left]
            dst_vertex[:, 1] = [top, top, bottom, bottom]  # [top, top, bottom, bottom]
            disturb_num = 0

            for k in range(0, self.disturb_time):
                context = 0.05
                smp_vertex = self.generate_disturb_rect(eye_rect, context, width, height)
                M = cv2.getPerspectiveTransform(smp_vertex, dst_vertex)

                wrap_img = cv2.warpPerspective(img, M, (width, height))
                left, top, right, bottom = int(left), int(top), int(right), int(bottom)
                wrap_img_roi = wrap_img[top:bottom + 1, left:right + 1]
                # print img.shape, wrap_img_roi.shape, left, top, right, bottom

                # fn = os.path.join(outimg_dir, "%06d.png" % k)
                _img_path, _img_name = os.path.split(img_name)
                if _img_path[0] == os.sep:
                    _img_path = _img_path[1:]
                if (img_idx % 10) in test_ratio:
                    w_img_path = append_diff_part_path(_img_path, self.save_path + 'test')
                else:
                    w_img_path = append_diff_part_path(_img_path, self.save_path + 'train')

                _img_name = os.path.splitext(_img_name)[0]
                fn = os.path.join('', w_img_path, _img_name + '_' + str(disturb_num) + '.png')
                print fn
                disturb_num += 1

                # Check if need to create save dir
                if img_idx == 0:
                    test_path = append_diff_part_path(_img_path, self.save_path + 'test')
                    train_path = append_diff_part_path(_img_path, self.save_path + 'train')
                    if not os.path.exists(test_path):
                        os.makedirs(test_path)
                    if not os.path.exists(train_path):
                        os.makedirs(train_path)
                    if not os.path.exists(w_img_path):
                        os.makedirs(w_img_path)

                cv2.imwrite(fn, wrap_img_roi)

            img_idx += 1


if __name__ == '__main__':
    args = parse_args()
    if not os.path.exists(args.save_path):
        if args.save_path[-1] == os.sep:
            args.save_path = args.save_path[:-1]
        print args.save_path, "not exists"
        raw_input('press any key to create it')
    b = B(args, 0)
    b.process()
