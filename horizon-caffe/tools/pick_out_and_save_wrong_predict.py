#! /use/bin/env python
# input file
# Model:
# version: 0
# data path: /home/fenghan/Videos/20170614_evaluating/dynamic_20170530_JOC_3/close/
# model path: ../etc/hanfeng_eyeclassify.fxnetmodel
#
# [9999_0_1189.png]	0:0.000854			1:0.999146			2:-0.000000			result:1
import os
import cv2


def save_wrong_pic(save_path, pic_name, pic_path):
    img = cv2.imread(os.path.join(pic_path, pic_name))
    cv2.imwrite(os.path.join(save_path, pic_name), img)


def show_wrong_pic(pic_path):
    img = cv2.imread(pic_path)
    cv2.namedWindow("Wrong_Predict_Image")
    cv2.imshow("Wrong_Predict_Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def pick_out_wrong_predict(test_result_file, wrong_predict_pic_save_path):
    with open(test_result_file, 'r') as result_file:
        for line in result_file.readlines():
            if line.find('data path'):
                pic_path = line.split()[-1]
                print pic_path
                ground_truth = str(pic_path).split('/')[-1]
                if ground_truth.find('close'):
                    ground_truth = 1
                elif ground_truth.find('open'):
                    ground_truth = 0
                else:
                    print 'The data path is wrong.'
                    return
            if line.find('result'):
                pic_name_begin_index = line.find('[')
                pic_name_end_index = line.find(']')
                pic_name = line[pic_name_begin_index:pic_name_end_index]
                result = line.split(':')[-1]
                if result != ground_truth:
                    print wrong_predict_pic_save_path + ' ' + pic_name + ' ' + pic_path
                    save_wrong_pic(wrong_predict_pic_save_path, pic_name, pic_path)


if __name__ == '__main__':
    print 'input the test_result_file path:'
    test_result_file_path = raw_input()
    print 'input the wrong predict pic save folder path:'
    save_path = raw_input()
    pick_out_wrong_predict(test_result_file_path, save_path)
