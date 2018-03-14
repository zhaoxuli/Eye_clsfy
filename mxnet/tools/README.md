# mxnet眼睛训练脚本说明
- [convert_caffeList_to_mxnetList](./convert_caffeList_to_mxnetList.py)
将caffe的数据列表转换成mxnet需要的lst格式
- [im2rec.py](./im2rec.py)
 将训练数据转换成rec类型
- [pick_epoch.py](./pick_epoch.py) 从训练产生log中选取一个最好的模型
- [predict.py](./predict.py) 对模型进行小批量预测
- [get_result_file.py](./get_result_file.py)  针对所有数据集进行预测
- [PR_new.py](./PR_new.py) 根据预测的结果验证模型性能
- [nhwc2nchw.py](./nhwc2nchw.py) 将模型转换成nchw类型