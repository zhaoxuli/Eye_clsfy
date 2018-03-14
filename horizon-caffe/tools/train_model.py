#! /usr/bin/env python

import os
import re
import random
import argparse
from third_party.caffe_tools import parse_log


def set_solver(filename, i):
    # snapshot_prefix: "models/eyeclassify_20170805"
    if not os.path.exists(filename):
        exit(-1)
    filename_new = filename + '.backup'
    if not os.path.exists(filename_new):
        os.rename(filename, filename_new)
    lines = open(filename_new).readlines()
    solver = open(filename, 'w')
    for s in lines:
        if s.find('snapshot_prefix: ') != -1:
            model = re.findall('"([^"]+)"', s)[0]
            solver.write(s.replace(model, model + '_' + str(i)))
        else:
            solver.write(s)
    solver.close()


def get_log(logfile_path):
    train_dict_list, test_dict_list = parse_log.parse_log(logfile_path)
    return train_dict_list, test_dict_list


def set_train_eva_file(train_file, n, i):
    file_list_path = os.path.dirname(train_file)
    with open(train_file, 'r') as file_in:
        file_all = file_in.readlines()
        file_all.sort()
        file_num = file_all.__len__()
        file_test_begin = int((float(i - 1) / float(n)) * file_num)
        file_test_end = int((float(i) / float(n)) * file_num)
        test_lst = file_all[file_test_begin:file_test_end]
        if abs(file_test_begin - 0) < 1e-9:
            train_lst = file_all[file_test_end:]
        elif i == n:
            train_lst = file_all[:file_test_begin]
        else:
            train_lst = file_all[:file_test_begin] + file_all[file_test_end:]

        print "train test lst", set(train_lst) & set(test_lst)
        fout = open(file_list_path + '/test_files.txt', 'w')
        for i in test_lst:
            fout.write('%s' % i)
        fout.close()

        fout = open(file_list_path + '/train_files.txt', 'w')
        random.seed(100)
        random.shuffle(train_lst)
        for i in train_lst:
            fout.write('%s' % i)
        fout.close()


def train(solver, data_file, n=4):
    os.chdir(os.path.dirname(solver))
    TOOLS = '/home/users/dawei.yang/caffe-hobot/bin/'
    train_sh = TOOLS + 'caffe.bin train --solver=' + solver + ' -gpu=0 2>&1 | tee '
    for i in range(n):
        set_train_eva_file(data_file, n, i + 1)
        set_solver(solver, i + 1)
        log_name = str(i) + '.log'
        os.system(train_sh + log_name)
        # get_log(log_name)
        print 'Finish ' + str(i + 1)


def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-train_sh', help='train_full.sh path')
    parser.add_argument('-solver', help='solver prototxt path')
    parser.add_argument('-data_file', help='train data file list path')
    parser.add_argument('-rounds', type=int, help='cross validation')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()
    # train_sh = args.train_sh
    solver = args.solver
    data_file = args.data_file
    rounds = args.rounds
    # train_sh = '/home/fenghan/work/hf_work_20170610/train_full.sh'
    # solver = '/home/fenghan/work/hf_work_20170610/eyeclassify_solver.prototxt'
    # data_file = '/home/fenghan/work/hf_work_20170610/file_list/files_all.txt'
    train(solver, data_file, rounds)
