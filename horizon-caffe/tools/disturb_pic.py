#-*- coding: UTF-8 -*-

# Read pictures from 5 pre-categorized folders respecitively, save the image name and its eye status into
# a txt file. Below are 5 types of pre-categorized folders:
# 'open', 'closed', 'uncertain', 'occlusion', 'invisible'

# usage: python sumUp_eye.py

import os, sys
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
    parser.add_argument('-source', type=str)
    parser.add_argument('-eye_res', type=str, help='result text')
    parser.add_argument('-save_path', type=str)
    parser.add_argument('-disturb_time', type=int, default=10, help='[o]')
    args = parser.parse_args()

    if args.save_path[-1] != os.sep:
        args.save_path += os.sep
    return args


def read_frame(cap, frameid):
    if cv2.__version__[0] == '3':
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameid)
    else:
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameid)
    return cap.read()


def skip_comments_and_blank(file, cm='#'):
    lines = list()
    for line in file:
        line = line.strip()
        if not line.strip().startswith(cm) and not line.isspace():
            lines.append(line)
    return lines


# frame_id x1 y1 width height x2 y2 width height
# 0.png 495 335 45 30 576 329 46 31
# 1.png 477 332 52 35 570 326 49 33
# 2.png 487 337 48 32 568 325 48 32
# 3.png 488 340 45 30 568 326 45 30
# 4.png 478 339 49 32 564 327 48 32
# 5.png 479 335 50 33 567 322 49 32
# 6.png 474 337 52 34 564 322 53 35
# 7.png 475 332 54 36 569 322 54 36
# 8.png 482 326 55 37 580 319 54 36
# 9.png 477 321 61 40 587 309 65 43
class B:
    def __init__(self, args, debug=0):
        self.pic_dir = args.pic_dir
        self.save_path = args.save_path
        self.disturb_time = args.disturb_time
        self.source = args.source
        self.eye_res = args.eye_res

        f = open(self.eye_res)
        comment = f.readline().strip()
        f.close
        cut_scale = comment.split(' ')[1]
        if cut_scale not in ['1.8x1.8', '1.5x1', '1.5x1.5']:
            print "Error:", cut_scale, "is not support now"
            exit()
        self.cut_scale = cut_scale
        if debug == 1:
            print 'args:', args

    def get_eye_rect(self, label, left_right):
        def convert_scale(m1, m2, n1, n2, left, right, top, bottom):
                w = (right - left) / float(m1)
                ox = (n1 - m1) * w / 2.0
                oy = (n2 - m2) * w / 2.0
                return left - ox, top - oy, right + ox, bottom + oy

        if left_right == 'right':
            left = float(label[0])
            right = left + float(label[2])
            top = float(label[1])
            bottom = top + float(label[3])
        elif left_right == 'left':
            left = float(label[4])
            right = left + float(label[6])
            top = float(label[5])
            bottom = top + float(label[7])

        if self.cut_scale == "1.8x1.8":
            pass
        elif self.cut_scale == "1.5x1":
            left, top, right, bottom = convert_scale(1.5, 1, 1.8, 1.8, left, right, top, bottom)
        elif self.cut_scale == "1.5x1.5":
            left, top, right, bottom = convert_scale(1.5, 1.5, 1.8, 1.8, left, right, top, bottom)

        return left, top, right, bottom

    def generate_disturb_rect(self, rect, context, img_w, img_h):
        import random
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        x0 = rect[0] - random.random() * w * context
        x1 = rect[2] + random.random() * w * context
        x2 = rect[2] + random.random() * w * context
        x3 = rect[0] - random.random() * w * context
        y0 = rect[1] - random.random() * w * context
        y1 = rect[1] - random.random() * w * context
        y2 = rect[3] + random.random() * w * context
        y3 = rect[3] + random.random() * w * context
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
        #for dir, algo_res_file, video in self.algofile_list:
        dir = self.pic_dir
        print "[Processing]", dir, self.eye_res, self.source

        ### 1. Open algo res
        f = open(self.eye_res)
        lines = skip_comments_and_blank(f)
        lines = map(lambda x: x.strip().split(), lines)

        ## "0.png" => 0
        frame_id_list = map(lambda x: int(x[0].split('.')[0]), lines)
        frame_res_list = map(lambda x: x[1:], lines)
        print 'Total %d frames and %d res' % (len(frame_id_list), len(frame_res_list))

        ### 2. Open video
        cap = cv2.VideoCapture(self.source);
        if not cap.isOpened():
            print "ERROR : the mp4 file open failed."
            raw_input('press any key to continue')
        
        if cv2.__version__[0] == '3':
            img_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            img_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            img_w = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
            img_h = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        print "video res", img_w, img_h

        #exit()
        ###
        src_files = glob.glob(dir + os.path.sep + '*')
        img_idx = 0
        for img_name in src_files:
            ## /Volumes/TF128-OV/uhome/DMS_Pic/20170418_JOC/12PM/1794856009/closed/left_10842.png => 10842
            frame_id = int(img_name.split(os.path.sep)[-1].split('.')[0].split('_')[-1])
            left_right = img_name.split(os.path.sep)[-1].split('.')[0].split('_')[0]
            idx = frame_id_list.index(frame_id)

            left, top, right, bottom = self.get_eye_rect(frame_res_list[idx], left_right)
            eye_rect = [left, top, right, bottom]
            ret, img = read_frame(cap, frame_id)
            #print "frame_id", frame_id

            dst_vertex = np.zeros((4, 2), dtype="float32")
            dst_vertex[:, 0] = [left, right, right, left]  # [left, right, right, left]
            dst_vertex[:, 1] = [top, top, bottom, bottom]  # [top, top, bottom, bottom]
            disturb_num = 0
            for k in range(0, self.disturb_time):
                context = 0.1
                smp_vertex = self.generate_disturb_rect(eye_rect, context, img_w, img_h)
                M = cv2.getPerspectiveTransform(smp_vertex, dst_vertex)

                wrap_img = cv2.warpPerspective(img, M, (img_w, img_h))
                left, top, right, bottom = int(left), int(top), int(right), int(bottom)
                wrap_img_roi = wrap_img[top:bottom+1, left:right+1]
                #print img.shape, wrap_img_roi.shape, left, top, right, bottom

                # fn = os.path.join(outimg_dir, "%06d.png" % k)
                _img_path, _img_name = os.path.split(img_name)
                if _img_path[0] == os.sep:
                    _img_path = _img_path[1:]
                if (img_id % 10) in test_ratio:
                    w_img_path = self.save_path + os.sep + 'test' + os.sep + _img_path
                else:
                    w_img_path = self.save_path + os.sep + 'train'+ os.sep + _img_path

                _img_name = os.path.splitext(_img_name)[0]
                fn = os.path.join('', w_img_path, _img_name+'_'+str(disturb_num)+'.png')
                disturb_num += 1
                
                # Check if need to create save dir
                if img_idx == 0:
                    test_path = self.save_path + os.sep + 'test' +  os.sep + _img_path
                    train_path = self.save_path + os.sep + 'train' + os.sep +  _img_path
                    print test_path
                    print train_path
                    print w_img_path
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
