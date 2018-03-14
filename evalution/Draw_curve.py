#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 17:02:38 2017

@author: zhaoxu
"""

# -*- coding:utf-8 -*-
# ! /usr/bin/env python
import Tkinter
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
#from sklearn.metrics import precision_recall_curve


# data path: /home/fenghan/Videos/dynamic_20170605_JOC/hobot946685174407/a_close
# model path: ../etc/eyeclassify_20170615_iter_30000.fxnetmodel
#
# [9999_0_16251.png]	0:0.000055			1:0.999945			2:-0.000490			result:1
#
# Image count = 				1099
# open eye count = 			2
# close eye count = 			1097
# uncertain eye count = 		0


def get_ground_truth(file):
    with open(file, 'r') as result_file:
        for line in result_file.readlines():
            if line.find('data path') != -1:
            # if line.find('data_path') != -1:
                label = str(line).split('/')[-1]
               # print label
                if label.find('close') != -1:
                    if label.find('glass') != -1:
                        return 1, 1
                    else:
                        return 1, 0
                elif label.find('open') != -1:
                    if label.find('glass') != -1:
                        return 0, 1
                    else:
                        return 0, 0
                else:
                    print 'false'


def get_data(dir):
    count = 0
    open_count = 0
    close_count = 0
    open_score0 = []
    open_score1 = []
    close_score1 = []
    close_erro_list = []
    glass_close_count = 0
    a_close_count = 0
    glass_close = 0
    a_close = 0
    glass_open_count = 0
    a_open_count = 0
    glass_open = 0
    a_open = 0
    for root, dirs, files in os.walk(dir):
    	#print root,files
    	#exit ()
        for file in files:
            #print os.path.join(root, file)
  #          exit ()
            ground_truth,has_glass = get_ground_truth(os.path.join(root, file))
            with open(os.path.join(root, file), 'r') as result_file:
                for line in result_file.readlines():
                    if line.find('data path') != -1:
                        data_path = line.split(':')[1][:-1]+os.sep
                        data_path = data_path.replace('/home/users/dawei.yang/data/','/mnt/hgfs/work/eye_data/source_eye_data/')
                    if line.find('result') != -1:
                        count += 1
                        confidence_open = float(line.split()[1].split(':')[-1])
                        confidence_close = float(line.split()[2].split(':')[-1])
                        if ground_truth == 0:
                            if has_glass:
                                glass_open += confidence_open
                                glass_open_count += 1
                            elif not has_glass:
                                a_open += confidence_open
                                a_open_count += 1
                            open_count += 1
                            if confidence_open <0.2:
                                close_erro_list.append(data_path + line.split()[0][1:-1])
                            open_score0.append(confidence_open)
                            open_score1.append(confidence_close)
                        elif ground_truth == 1:
                            if has_glass:
                                glass_close += confidence_close
                                glass_close_count += 1
                            elif not has_glass:
                                a_close += confidence_close
                                a_close_count += 1
                            close_count += 1
                            close_score1.append(confidence_close)
    print 'mean_glass_close_score = %.3f' % (float(glass_close) / glass_close_count)
    print 'mean_a_close_score = %.3f' % (float(a_close) / a_close_count)
    print 'mean_glass_open_score = %.3f' % (float(glass_open) / glass_open_count)
    print 'mean_a_open_score = %.3f' % (float(a_open) / a_open_count)
    print 'a_open_count, glass_open_count, glass_close_count, a_close_count'
    print a_open_count, glass_open_count, glass_close_count, a_close_count
    print len(close_erro_list)
    #print close_erro_list[0]
    return count, open_count, close_count, open_score0, open_score1, close_score1


def get_status(threshold, value):
    if value >= threshold:
        return 1
    else:
        return 0


def draw_curve(dir):
    count, open_count, close_count, open_score0, open_score1, close_score1 = get_data(dir)
    print  'count, open_count, close_count'
    print count, open_count, close_count
    print 'close_scor       ' ,len (close_score1)
    print 'open_score1       ', len(open_score1)
    open_score0_dist = []
    close_score1_dist = []
    for i in np.arange(0, 1.0, 0.1):
        num = 0
        if i == 0.9:
            for n in open_score0:
                if (n >= i) and (n <= (i + 0.1)):
                    num += 1
        else:
            for n in open_score0:
                if (n >= i) and (n < (i + 0.1)):
                    num += 1
        open_score0_dist.append(float(num) / open_count)
   # print open_score0_dist

    for i in np.arange(0, 1.0, 0.1):
        num = 0
        if i == 0.9:
            for n in close_score1:
                if (n >= i) and (n <= (i + 0.1)):
                    num += 1
        else:
            for n in close_score1:
                if (n >= i) and (n < (i + 0.1)):
                    num += 1
        close_score1_dist.append(float(num) / close_count)
    #print close_score1_dist

    accuracy_close_threshold = []
    for i in np.arange(0, 1.1, 0.1):
        num = 0
        for x in open_score1:
            if x < i:
                num += 1
        for y in close_score1:
            if y >= i:
                num += 1
        accuracy_close_threshold.append(float(num) / count)
    plt.figure(4)
    plt.title('PR')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.grid(True)
    img_inf = []
    info_list=[]
#        for i in range(len(ground_truth_list)):
#        info_split={'score':float(normal_score_list[i]),'truth':int(ground_truth_list[i])}
#        info_list.append(info_split)
   # y_true = []
   # y_scores = []
    for y in close_score1:
        img = {'label': 1, 'score0': 1 - y, 'score1': y}
        img_inf.append(img)
        info_split={'score1':float(y),'label':int(1)}
        info_list.append(info_split)
       # y_scores.append(y)

    #for i in range(close_count):
    for x in open_score1:
        #x = float(x)
        img = {'label': 0, 'score0': 1 - x, 'score1': x}
        img_inf.append(img)
        info_split={'score1':float(x),'label':int(0)}
        info_list.append(info_split)

    sorted_img_inf=sorted(info_list,key=lambda x:x['score1'],reverse=True)
    print ("|  %-8s  | %-8s | %8s | %-8s | %-20s | %-4s |    " % (
    "TP", "FP", "FN", "TN",'ap','threshold'))
    for j in np.arange(0.1, 1.0, 0.1):
        P = []
        R = []
        TP = 0  # label: close, predict: close
        FP = 0  # label: open, predict: close
        FN = 0  # label: open, predict: open
        TN = 0
        for img in sorted_img_inf:
            if (img['label'] == 1) and (img['score1'] >= j):
                TP += 1
            elif (img['label'] == 1) and (img['score1'] < j):
                FN += 1
            elif (img['label'] == 0) and (img['score1'] >= j):
                FP += 1
            elif (img['label'] == 0) and (img['score1'] < j):
                TN += 1
            if (TP + FP) == 0:
                P.append(1)
                R.append(0)
            else:
                P.append(float(TP) / float(TP + FP))
                R.append(float(TP) / close_count)
        # plt.plot(R, P, label='close threshold' + str(i))
        # plt.legend(loc='center left')
        #print 'TP',TP,'FP',FP,'FN',FN,'TN',TN

        p_new=[0.00]+P
        for i in range(len(p_new)-2,0,-1):
            p_new[i]=max(p_new[i],p_new[i+1])
        r_new=[0]+R
        ap = 0
        for i in xrange(len(p_new)-1):
            if p_new[i+1] > 0.8: #0.9:
                ap += (r_new[i+1] - r_new[i])*p_new[i+1]
#        #print 'ap=',ap,'             ','threshold=',j
        #ap=np.trapz(p_new,r_new)
        #ap=float(sum(p_new)/len(r_new))
        print ("|  %-8s  | %-8s | %8s | %-8s | %-20s | %-9s |    " % (
        TP,FP,FN,TN,ap,j))
        if j==0.8:
        #print TP_normal,FP_normal,FN_normal,TN_normal,ap
            p_new=p_new[1:]
            r_new=r_new[1:]
            plt.plot(r_new, p_new,'b', label='PR')
            plt.xlim(0,1,0.1)
            plt.ylim(0.95,1)
            plt.legend(loc='center left')
    #p_new=sorted(P)

        #print R
        # plt.scatter(R, P)

    x_values = np.arange(0.05, 1.05, 0.1)
    #x_values_2 = np.arange(0, 1.1, 0.1)
    x_values_2 = np.arange(0, 1.1, 0.1)

    plt.figure(1)
    # plt.plot(x_values, open_score0_dist)
    plt.bar(x_values, open_score0_dist,  width = 0.1 ,facecolor='lightskyblue', edgecolor='white')
    plt.xlim(0, +1.0)

    for x, y in zip(x_values, open_score0_dist):
        plt.text(x , y, '%.3f' % y, ha='center', va='bottom')
    plt.title('Open distribution')
    plt.xlabel('Probability')
    plt.ylabel('Num')
    plt.grid(True)

    plt.figure(2)
    # plt.plot(x_values, close_score1_dist)
    plt.bar(x_values, close_score1_dist, width=0.1, facecolor='lightskyblue', edgecolor='white')
    plt.xlim(0, +1.0)
    for x, y in zip(x_values, close_score1_dist):
        plt.text(x, y, '%.3f' % y, ha='center', va='bottom')
    plt.title('Close distribution')
    plt.xlabel('Probability')
    plt.ylabel('Num')
    plt.grid(True)

    plt.figure(3)
    plt.plot(x_values_2, accuracy_close_threshold)
    for x, y in zip(x_values_2, accuracy_close_threshold):
        plt.text(x, y - 0.03, '%.3f' % y, ha='center', va='bottom')
    plt.title('Accuracy')
    plt.xlabel('Close threshold')
    plt.ylabel('Accuracy')
    plt.grid(True)

    # plt.figure(4)
    # plt.plot(R, P)
    # plt.title('PR')
    # plt.xlabel('Recall')
    # plt.ylabel('Precision')
    # plt.grid(True)

    plt.show()
    return sorted_img_inf

if __name__ == '__main__':
    img=[]
    # dir = raw_input('enter the dir path of eyeclassify_output_file: ')
    dir =  sys.argv[1]
    draw_curve(dir)
    #count, open_count, close_count, open_score0, open_score1, close_score1 = get_data(dir)
