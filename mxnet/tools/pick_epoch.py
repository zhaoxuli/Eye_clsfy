import os 
import sys
log_file_path =  sys.argv[1]
#log_file_path = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/cifar_10/Gap/1030.log'

#1channel  3conv  drop_out
test_list = []
train_list = []

with open(log_file_path, 'r') as log_file:
	for  line  in log_file.readlines():
		if 'Epoch' in line:
			# epoch = line.split(']')[0].split('[')[-1]
			# num = int(epoch)-1
			# print num
			if 'Validation-accuracy' in line:
				test_score = float(line.split('=')[-1])
				test_list.append(test_score)
			if 'Train-accuracy' in line:
				train_score = float(line.split('=')[-1])
				train_list.append(train_score)

info_list = {}
info_list = {'test_score':test_list,'train_score':train_list}

score_list = []
index_list = []
sort_list = []

for i in range(len(test_list)):
	info_score= 0.9*float(info_list['test_score'][i])# +0.1* float(info_list['train_score'][i])
	score_list.append(info_score)
sort_list = sorted(score_list,reverse = True)
for i in range(len(sort_list)):
        index_num=score_list.index(sort_list[i])
        index_list.append(index_num)
#print index_list
for i in range(10):
        print 'epoch_num: ',index_list[i]+1 , \
        	' test_acuuracy: ' ,test_list[index_list[i]]  ,  \
        	'    train_accuracy:  ' ,train_list[index_list[i]]
