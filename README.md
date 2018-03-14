# Eyeclassify 训练说明
训练框架采用了两种，horizon-caffe 和 mxnet
，训练时的数据预处理过程可以参考[my_preprocess.ipynb](./horizon-caffe/tools/my_preprocess.ipynb)
* horizon-caffe  
已停止更新，现已使用Mxnet训练模型
* Mxnet
[tools](./mxnet/tools/)中存放预测工具，以及模型性能验证脚本
*  data_set
中存放训练的原始数据路径，对应的txt为各个服务器名称
* test_data  
 中存放待验证图片，用于单张验证

## Environment_Setup
*  yz-gpu026.hogpu.cc   `$ source env_yz-gpu026.sh`

## Config Run_eye.sh

```{.python .input  n=12}
!ls  ./example
#cp  ./example/Run_eye.sh.example   .example/Run_eye.sh
```

修改其中的    `TRAIN_PATH`,  `DATA_PATH`,  `OUTPUT_PATH`,  `NET_Type`参数


##  运行

```{.python .input  n=14}
!bash  ./example/Run_eye.sh
```
## 评测模型性能
```
$cd   ./evalution
$ python get_reslut.py  model_path  best_epoch_num  result_folder
$ python draw_curve.py  result_folder
```
各个脚本作用，参考[./evalution/readme.md](./evalution/readme.md)