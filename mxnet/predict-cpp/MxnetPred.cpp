#include <vector>
#include <iostream>
#include <fstream>
#include <cassert>
#include "MxnetPred.h"

// Path for c_predict_api
#include <mxnet_predict/c_predict_api.h>


// Read file to buffer
class BufferFile {
public :
    std::string file_path_;
    int length_;
    char* buffer_;

    explicit BufferFile(std::string file_path)
            :file_path_(file_path) {

        std::ifstream ifs(file_path.c_str(), std::ios::in | std::ios::binary);
        if (!ifs) {
            std::cerr << "Can't open the file. Please check " << file_path << ". \n";
            length_ = 0;
            buffer_ = NULL;
            return;
        }

        ifs.seekg(0, std::ios::end);
        length_ = ifs.tellg();
        ifs.seekg(0, std::ios::beg);
        std::cout << file_path.c_str() << " ... "<< length_ << " bytes\n";

        buffer_ = new char[sizeof(char) * length_];
        ifs.read(buffer_, length_);
        ifs.close();
    }

    int GetLength() {
        return length_;
    }
    char* GetBuffer() {
        return buffer_;
    }

    ~BufferFile() {
        if (buffer_) {
            delete[] buffer_;
            buffer_ = NULL;
        }
    }
};




MxnetPred::~MxnetPred()
{
    // Release Predictor
    if( mp_pred_hnd != NULL )
        MXPredFree(mp_pred_hnd);
}


int MxnetPred::init(std::string json_file, std::string param_file, int width, int height, int channels)
{
    m_width = width;
    m_height = height;
    m_channels = channels;

	BufferFile json_data(json_file);
    BufferFile param_data(param_file);

    // Parameters
    const int dev_type = 1;  // 1: cpu, 2: gpu
    const int dev_id = 0;  // gpu device id
    const mx_uint num_input_nodes = 1;  // 1 for feedforward
    const char* input_key[1] = {"data"};
    const char** input_keys = input_key;

    const mx_uint input_shape_indptr[2] = { 0, 4 };
    // const mx_uint input_shape_data[4] = { 1,
    //                                     static_cast<mx_uint>(m_channels),
    //                                     static_cast<mx_uint>(m_height),
    //                                     static_cast<mx_uint>(m_width)};
    const mx_uint input_shape_data[4] = { 1,
                                        static_cast<mx_uint>(m_height),
                                        static_cast<mx_uint>(m_width),
                                        static_cast<mx_uint>(m_channels)};


    if (json_data.GetLength() == 0 ||
        param_data.GetLength() == 0) {
        return -1;
    }

    // Create Predictor
    MXPredCreate((const char*)json_data.GetBuffer(),
                 (const char*)param_data.GetBuffer(),
                 static_cast<size_t>(param_data.GetLength()),
                 dev_type,
                 dev_id,
                 num_input_nodes,
                 input_keys,
                 input_shape_indptr,
                 input_shape_data,
                 &mp_pred_hnd);

    assert(mp_pred_hnd);


    m_img_data.resize(m_width*m_height*m_channels);
    std::cout<< m_width*m_height*m_channels<<std::endl;

	return 0;
}

/// Make sure the order of p_mean is same with image_data,
/// that is if image_data restores as B-G-R, the same as p_mean
// int MxnetPred::predict(const char *image_data, const float *p_mean, std::vector<float> &pred_res)
// {
//     const int image_area = m_height * m_width;

//     if( (image_data == NULL) || (p_mean == NULL) )
//         return -1;

//     /// Minus mean
//     float *ptr_image = m_img_data.data();
//     const float *ptr_mean = p_mean;
//     if (m_channels == 3) {
//         for (int i = 0; i < image_area; i++) {
//             *ptr_image++ = static_cast<mx_float>(*image_data++) - *ptr_mean++;
//             *ptr_image++ = static_cast<mx_float>(*image_data++) - *ptr_mean++;
//             *ptr_image++ = static_cast<mx_float>(*image_data++) - *ptr_mean++;
//         }
//     }
//     else{
//         float *ptr_image = m_img_data.data();
//         for (int i = 0; i < m_channels * m_width; i++) {
//             *ptr_image++ = static_cast<mx_float>(*image_data++) - *ptr_mean++;
//         }
//     }

//     do_predict(pred_res);
// }

/// Make sure the order of p_mean is same with image_data,
/// that is if image_data restores as B-G-R, the same as p_mean
int MxnetPred::predict(const uint8_t *image_data, std::vector<float> &mean, std::vector<float> &pred_res)
{
    const int image_area = m_height * m_width;
    std::cout<<"image_area"<<image_area<<std::endl;
    if (image_data == NULL)
        return -1;
    else if (m_channels != mean.size())
        return -2;

    /// Minus mean
    float *ptr_image = m_img_data.data();
    if (m_channels == 3) {
        for (int i = 0; i < image_area; i++) {
            *ptr_image++ = static_cast<mx_float>(*image_data++) - mean[0];
            *ptr_image++ = static_cast<mx_float>(*image_data++) - mean[1];
            *ptr_image++ = static_cast<mx_float>(*image_data++) - mean[2];
        }
    } else {
    	std::cout<<"here "<<image_area<<std::endl;
        float *ptr_image = m_img_data.data();
        for (int i = 0; i < image_area; i++) {
          *ptr_image = (static_cast<mx_float>(*image_data) - mean[0]);
          //printf("%f, %f\n", *ptr_image++, (float)(char)(*image_data++));

        }
    }

    do_predict(pred_res);

    return 0;
}

void MxnetPred::do_predict(std::vector<float> &pred_res)
{
    const int image_size = m_channels * m_width * m_height;

    /// Set Input Image
    MXPredSetInput(mp_pred_hnd, "data", m_img_data.data(), image_size);

    /// Do Predict Forward
    MXPredForward(mp_pred_hnd);

    mx_uint output_index = 0;
    mx_uint *shape = 0;
    mx_uint shape_len;

    /// Get Output Result
    MXPredGetOutputShape(mp_pred_hnd, output_index, &shape, &shape_len);

    size_t size = 1;
    for (mx_uint i = 0; i < shape_len; ++i)
        size *= shape[i];

    pred_res.resize(size, 0);
    MXPredGetOutput(mp_pred_hnd, output_index, pred_res.data(), size);
}


#include <opencv2/opencv.hpp>

int main(int argc, char* argv[]) {
    if (argc < 5) {
        std::cout << "argc =" << argc << std::endl
                  << "Usage: ./image-classification-predict apple.jpg json_file.json param_file.params synset_file [mean_file.nd]"
                  << std::endl;
        return 0;
    }

    std::string test_file;
    test_file = std::string(argv[1]);

    /// Models path for your model, you have to modify it
    std::string json_file = argv[2];
    std::string param_file = argv[3];
    std::string synset_file = argv[4];
    std::string nd_file = "";
    if (argc == 6)
        nd_file = argv[5];

    /// Image size and channels
    const int width = 32;
    const int height = 32;
    const int channels = 1;
    int image_size = width * height * channels;

    /// Read Image Data
    std::vector<mx_float> image_data = std::vector<mx_float>(image_size);
    const int color_flag = cv::IMREAD_COLOR ? (channels == 3) : cv::IMREAD_GRAYSCALE;
    cv::Mat mSrc = cv::imread(test_file, color_flag);
    printf("mSrc = %dx%dx%d\n", mSrc.channels(), mSrc.cols, mSrc.rows);
    cv::Mat mRsz(32, 32, CV_8UC1);
    bool isCon = mRsz.isContinuous();
    if(isCon)
    	printf("continue %d\n", 1);
    else
    	printf("continue %d\n", 0);

    cv::resize(mSrc, mRsz, cv::Size(width, height));
    printf("mRsz = %dx%dx%d\n", mSrc.channels(), mRsz.cols, mRsz.rows);
    std::vector<float> mean(channels);
    std::vector<float> pred_res;
    MxnetPred mxnetPred;

    if (channels == 3) {
        mean[0] = 0;
        mean[1] = 0;
        mean[2] = 0;
    }
    else {
        mean[0] = 0;
    }

    int ret = mxnetPred.init(json_file, param_file, width, height, channels);
    if(ret != 0) std::cout << "mxnetPred.init failed " << ret << std::endl;
    ret = mxnetPred.predict((const uint8_t*)mRsz.data, mean, pred_res);
    if(ret != 0) std::cout << "mxnetPred.predict failed " << ret << std::endl;

    std::cout << "pred_res: " << pred_res.size() << std::endl;
    for ( int i = 0; i < static_cast<int>(pred_res.size()); i++ ) {
        printf("Accuracy[%d] = %.8f\n", i, pred_res[i]);
    }

    return 0;
}
