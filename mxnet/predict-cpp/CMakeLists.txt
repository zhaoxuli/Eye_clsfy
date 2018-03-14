cmake_minimum_required(VERSION 2.8)
    
project(mxnet_predict_test)

#set(MXNET_SOURCE_PATH "~/.gradle/caches/modules-2/files-2.1/com.hobot.native/mxnet_predict/1.2.1_linux/files/mxnet_predict")
set(MXNET_SOURCE_PATH "/home/users/dawei.yang/zhaoxu.li/mxnet_face_yuxi_my")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
#set(Opencv_source_path "/home/zhaoxu/dms_test/dms/prebuilds/linux-x86/cv3.2")
set(OPENCV_PATH "/home/users/dawei.yang/opencv3.2")

set(HOBOTCORE_PATH "/home/zhaoxu/.gradle/caches/modules-2/files-2.1/com.hobot.native/hobot_core/0.1.0_linux/files/hobot_core")
set(BLAS_PATH "/home/zhaoxu/.gradle/caches/modules-2/files-2.1/com.hobot.native.base/hobot_blas/0.0.1_linux/files/hobot_blas/")

set( SOURCE_FILES
    MxnetPred.cpp
)

include_directories(
    ${MXNET_SOURCE_PATH}/include
    ${OPENCV_PATH}/include
    ${HOBOTCORE_PATH}/include
    ${BLAS_PATH}/include
)

link_directories(
    ${MXNET_SOURCE_PATH}/lib
    #${OPENCV_PATH}
    ${HOBOTCORE_PATH}/lib
    ${BLAS_PATH}/lib
)

add_executable(${PROJECT_NAME} MxnetPred.cpp)

target_link_libraries( 
    ${PROJECT_NAME} 
    mxnet
    #-Wl,--whole-archive libmxnet_predict.a  -Wl,--no-whole-archive
    #opencv_world
    /lib64/libopencv_core.so.2.4
    /lib64/libopencv_highgui.so.2.4
    /lib64/libopencv_imgproc.so.2.4
    #hobot_core
    #hobot_blas
    #/home/zhaoxu/.gradle/caches/modules-2/files-2.1/com.hobot.native.hobot/hobot/1.3.6_linux/files/hobot/lib/libhobotthread.a
)
