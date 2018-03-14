import mxnet as mx
import argparse
import numpy as np
from collections import namedtuple
import cv2
import os
import sys


#python  get_result_file.py  model   epoch  out_dir_name
print  'python  get_result_file.py  model   epoch  out_dir_nam'

model_version = ''
data_path =  '/home/users/dawei.yang/data/data_1106/'
model_url =  sys.argv[1]
#model_url = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/cifar_10/1channel//models/model'

out_dir_name = sys.argv[3]

epoch = sys.argv[2]
epoch =  int(epoch)
out_dir_path = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/result_compare/'



def get_result(model_url, epoch, img_url):

	Batch = namedtuple('Batch', ['data'])
#initialize mod
	sym, arg_params, aux_params = mx.model.load_checkpoint(model_url, epoch)
	mod = mx.mod.Module(symbol=sym, context=mx.cpu(), label_names=None)
	mod.bind(for_training=False, data_shapes=[('data', (1,1,32,32))],
		label_shapes=mod._label_shapes)
	mod.set_params(arg_params, aux_params, allow_missing=True)
#get img reshape img to  bacth,channel,h,w
	img = cv2.imread(img_url)

	img = img[:,:,0]
	img = cv2.resize(img,(32,32))

	img = img[np.newaxis, :]
	img = img[np.newaxis, :]

	mod.forward(Batch([mx.nd.array(img)]))
#do predict
	prob = mod.get_outputs()[0].asnumpy()
	open_score = prob[0][0]
	close_score = prob[0][1]
	if (open_score - close_score) > 0:
		if open_score > 0.6:
			result = '0'
		else :
			result = '2'
	else:
		result = '1'
	#score is open score
	return  result,open_score

def get_file_list(data_dir):
	key_dirs = []
	dir_type = 'a_open|glass_open|a_close|glass_close'
	sub_dirs = os.walk(data_dir)
	key_type = dir_type.split('|')
	for sub_dir_files in sub_dirs:
		sub_dir = sub_dir_files[0]
		if sub_dir.split(os.sep)[-1] in key_type:	    	        
			All_img = os.listdir(sub_dir)
			#print sub_dir,len(All_img)
			key_dirs.append(sub_dir)
	return key_dirs

def  get_small_scale(open_score ):
	if (open_score < 0.0001):
		open_score = 0.0001
	if ((1 - open_score) < 0.0001 ):
		open_score = 0.9999
	return open_score





if __name__ == '__main__':

	num = 0
	#mkdir  a  output dir
	if os.path.exists('./' + out_dir_name) == False :
		os.mkdir('./' + out_dir_name)
	else:
		print   out_dir_name +"   is  existed"
	#do predict 
	key_dirs = get_file_list(data_path)
	for ele in key_dirs:
		print ele, '                  ',str(num)+'.txt'
		#ele = key_dirs[1]
			#  new txt 
		file_name = out_dir_path+os.sep + out_dir_name + os.sep + str(num) + '.txt'
		file = open(file_name, 'w')
		init_cont = 'Model:' + model_url + '\n' + 'Version:' +model_version +'\n'\
					+'data path:'+ele+'\n'+'model path:'+'\n'+'\n'+'\n'
		file.write(init_cont)
		# predit_result write in file
		All_img = os.listdir(ele)

		for img in All_img:
			result,open_score = get_result(model_url, epoch ,ele+os.sep+img)
			open_score = get_small_scale(open_score)
			open_score = round(open_score,4)
			context = ("%-50s  %-20s  %-20s  %-20s  %s  " \
					%('['+img+']','0:'+str(open_score),'1:'+str(1-open_score),'2:undetermined','result:'+str(result)))+'\n'

			file.write(context)
		num = int(num)+1

		# ending up 
		end_cont = '\n'+'\n'+'\n'+\
				   'Image_count=   '+str(len(All_img))+'\n'\
				   'open eye count=  '+'undetermined'+'\n'\
				   'close eye count=  '+'undetermined'+'\n'\
				   'open_scale =  '+'undetermined'+'\n'\
				   'close_scale =  '+'undetermined'+'\n'\
				   'uncertain_scale =  '+'undetermined'+'\n'
		file.write(end_cont)
		file.close
