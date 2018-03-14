**bn_ec.py**   is a  normal 3conv symbol cause the images is  the  singal channal  cut down the num_filters to 64.16.16.<p>
**Gap_ec.py**    is   Global_Average_Pooling  Network   after 3conv  lays  use double 1*1  conv  to fitting nonlinear  and  reduce dimsion after that use the 
max and  avg pooling get the class num  you want  send  result   to  softmax get score of each classes.
