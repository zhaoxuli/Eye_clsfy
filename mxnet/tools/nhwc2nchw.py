import os,sys
default_mxnet_path = "/home/users/yuxi.feng/Project/FaceAttr/mxnet_face/"
sys.path.insert(0, os.path.join(default_mxnet_path, 'python'))
import mxnet as mx
import numpy as np

def nhwc2nchw(params_file):
    params = mx.nd.load(params_file)
    out_params_file =  params_file + "_nchw"
    out_params = {}
    for k, v in params.items():
        t, name = k.split(':', 1)
        #print(name, v.asnumpy().shape)
        if (name.startswith("alphaconvolution") or name.startswith("conv") or name.startswith("fc") or name.startswith("residual_conv")) and (name.endswith("_weight")):
            arr = v.asnumpy()
            new_arr = np.swapaxes(np.swapaxes(arr, 1, 3), 2, 3)
            new_nd = mx.nd.empty(new_arr.shape, dtype=v.dtype)
            new_nd[:] = new_arr[:]
            print(k, v.shape, " to ", new_nd.shape)
            out_params[k]= new_nd
        else:
            print('ignore ', k)
            out_params[k]=v
    mx.nd.save(out_params_file, out_params)

if __name__ == "__main__":
    nhwc2nchw(sys.argv[1])
