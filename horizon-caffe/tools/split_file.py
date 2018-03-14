#! /usr/bin/python
# -*- coding: UTF-8 -*-

import os
import random


def split_file_to_train_and_test(file):
    with open(file, 'r') as file_in:
        file_all = file_in.readlines()
        file_num = file_all.__len__()
        file_num_train = int(file_num * 0.8)
        file_num_test = file_num - file_num_train
        print str(file_num) + ',' + str(file_num_train) + ',' + str(file_num_test)
        random.seed(100)
        random.shuffle(file_all)
        fout = open('../glass_classify/file_list/files_for_training.txt', 'w')
        for i in range(file_num_train):
            file_name = file_all[i]
            fout.write('%s' % file_name)
        fout.close()

        fout = open('../glass_classify/file_list/files_for_evaluating.txt', 'w')
        for i in range(file_num_test):
            file_name = file_all[file_num_train + i]
            fout.write('%s' % file_name)
        fout.close()

if __name__ == '__main__':
    split_file_to_train_and_test('../glass_classify/file_list/train_test_files.txt')
