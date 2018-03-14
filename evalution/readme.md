# evalution 脚本说明
`get_result.py`  
 该脚本是通过训练结束后选取的best_ecpoch model 进行全数据集的验证，  
 给出两类的得分，data的每一个folder结果都以一个txt文本保存在out_folder中。  
 `precict_folder.py`  
该脚本是用作单张/单个文件夹验证，用于验证有问题的单张图片，或者是有问题的图片集。  
`Draw_curve.py`  
根据`get_result.py`输出的txt结果画出：   
1.`正反两类得分的直方图 `  
2.` acc & threshhold `  
3.`   ap`