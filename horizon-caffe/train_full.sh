#!/usr/bin/env sh
set -e

#TOOLS=/home/users/dawei.yang/projects/eyeparsing/caffe-master/build/tools
TOOLS=/home/users/dawei.yang/caffe-hobot/bin
      
#$TOOLS/caffe.bin train \
#    --solver=/home/users/dawei.yang/projects/eyeclassify1/eyeclassify_solver.prototxt --gpu=1 $@

$TOOLS/caffe.bin train \
    --solver=eyeclassify_solver.prototxt   --gpu=1  2>&1  |tee 1012_morning.log
# --solver=/home/users/dawei.yang/projects/eyeclassify/eyeclassify_solver.prototxt --snapshot=examples/eyeclassify/cifar10_full_iter_60000.solverstate.h5 $@

# reduce learning rate by factor of 10
#$TOOLS/caffe train \
#    --solver=examples/eyeclassify/cifar10_full_solver_lr1.prototxt \
#    --snapshot=examples/eyeclassify/cifar10_full_iter_60000.solverstate.h5 $@

# reduce learning rate by factor of 10
#$TOOLS/caffe train \
#    --solver=examples/eyeclassify/cifar10_full_solver_lr2.prototxt \
#    --snapshot=examples/eyeclassify/cifar10_full_iter_65000.solverstate.h5 $@
