#  眼睛状态检测脚本使用说明
### Notice: 数据的处理过程（caffe，mxnet所需要的训练数据）可以参考[my_preprocess.ipynb](./my_preprocess.ipynb)的流程

- [convert_caffeList_to_mxnetList](./convert_caffeList_to_mxnetList.py)

将Caffe的数据集列表转换为MXNet需要的lst的格式

- [count_files](./count_files.py)

统计*a_open|glass_open|a_close|glass_close*每类的数量

- [data_list](./data_list.py)

列出每一个子数据集文件夹包含的*a_open|glass_open|a_close|glass_close*图片数量，详见[眼睛数据集列表](http://wiki.hobot.cc/pages/viewpage.action?pageId=16154653)

- [disturb_in_eye_pic](./disturb_in_eye_pic.py)

生成扰动图片，输入是眼睛区域的图片

- [disturb_in_pic](./disturb_in_pic.py)

生成扰动图片，输入是整幅图片，需要eyes.txt

- [disturb_on_multi_cpus](./disturb_on_multi_cpus.py)

多线程生成扰动图片

- [disturb_pic](./disturb_pic.py)

生成扰动图片，输入是视频，需要eyes.txt

- [generate_eye_info_json](./generate_eye_info_json.py)

将工程跑出来，然后人工筛选的图片生成为*json*文件，包含了眼睛区域的信息，以便他人或今后使用，详见[眼睛数据集列表](http://wiki.hobot.cc/pages/viewpage.action?pageId=16154653)

- [get_eyes_from_anno](./get_eyes_from_anno.py)

从标注的*json*文件里找到眼睛区域的信息，并从图片中截取眼睛区域的图像

- [get_landmarks_from_anno](./get_landmarks_from_anno.py)

从标注的*json*文件里找到landmark的信息

- [H264_to_mp4](./H264_to_mp4.py)

批量将一个目录中的h264格式的视频转为mp4格式

- [list_train_files](./list_train_files.py)

列出数据集每张图片的路径

- [list_train_folders](./list_train_folders.py)

列出每个*a_open|glass_open|a_close|glass_close*文件夹的路径

- [my_preprocess](./my_preprocess.ipynb)

从原始的眼睛区域的图像经过扰动-生成数据集列表-进行训练的处理训练流程脚本

- [plot_curve](./plot_curve.py)

根据[眼睛状态预测单元测试工具](http://njdrive01.hobot.cc/HanFeng/EyeClassifyFxnetModel)输出的结果生成模型评估曲线，详见[睁闭眼状态检测模型评估](http://wiki.hobot.cc/pages/viewpage.action?pageId=17796836)

- [preprocess](./preprocess.ipynb)

从原始的视频数据中经过扰动-生成数据集列表-进行训练的处理训练流程脚本

- [remove_score](./remove_score.py)

将图片文件名中的睁闭眼状态score值删除

- [rename](./rename.py)

将工程跑出来的眼睛图片的文件名重命名，生成扰动图片前需要做

- [show_json_data_on_img](./show_json_data_on_img.py)

将*json*中的landmark信息打在图片上并显示

- [show_pic_by_frame_id](./show_pic_by_frame_id.py)

通过帧号查看视频中的具体帧

- [sort_eyeclassify_output_file](./sort_eyeclassify_output_file.py)

将[眼睛状态预测单元测试工具](http://njdrive01.hobot.cc/HanFeng/EyeClassifyFxnetModel)的输出结果重新排序，其中的绘制曲线的部分已由[plot_curve](./plot_curve.py)代替

- [split_file](./split_file.py)

将数据集文件分为训练集和测试集两个文件

- [train_model](./train_model.py)

通过每次将数据集分为不同的训练集和测试集实现N折交叉验证

- [update_eye_train_data_with_new_face_lmk_model](./update_eye_train_data_with_new_face_lmk_model.py)

将用新的人脸检测和landmark模型截取出来的眼睛区域的图像替换掉之前人工筛选的图片，新的目录结构需要与之前的相同

**reference by feng.han**