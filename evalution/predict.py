import mxnet as mx
import argparse
import numpy as np
from collections import namedtuple
import cv2
import os
import  sys

print  mx.__path__
model_version = ''
model_url =  sys.argv[1]
#model_url = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/cifar_10/model_zoo/mobielnet_model'
#model_url = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/cifar_10/1channel/models/model'
#model_url = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/cifar_10/3conv/models/model'
#model_url = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/cifar_10/drop_out//models/model'

epoch =  sys.argv[2]
epoch = int(epoch)
out_dir_path = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/result_compare/'
img_url_dir = '/home/users/dawei.yang/data/data_train/Anno0905/10178/glass_open'

result_list = []

img_all =  os.listdir(img_url_dir)
for ele in img_all:
    img_url =  img_url_dir+ os.sep +ele
    Batch = namedtuple('Batch', ['data'])#initialize mod
    sym, arg_params, aux_params = mx.model.load_checkpoint(model_url, epoch)
    mod = mx.mod.Module(symbol=sym, context=mx.cpu(), label_names=None)
    mod.bind(for_training=False, data_shapes=[('data', (1,1,32,32))],
             label_shapes=mod._label_shapes)
    mod.set_params(arg_params, aux_params, allow_missing=True)
    #get img reshape img to  bacth,channel,h,w
    img = cv2.imread(img_url, 0)
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #img = img[:,:,0]
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
            result = '0'
        print  img_url_dir+ele,'         ',open_score
    else:
        result = '1'
    result_list.append(int(result))
#print float(sum(result_list)/len(img_all
print float(sum(result_list))/float(len(img_all)),model_url.split('/')[-2:]
print result_list
