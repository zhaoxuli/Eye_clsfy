//
// Created by austin on 7/19/17.
//

#ifndef DMS_MXNETPRED_H_H
#define DMS_MXNETPRED_H_H

#include <vector>

class MxnetPred{
private:
    void do_predict(std::vector<float> &pred_res);

public:
    ~MxnetPred();
    int init(std::string json_file, std::string param_file, int width, int height, int channels);
    int predict(const uint8_t *image_data, const float *p_mean, std::vector<float> &data);
    int predict(const uint8_t *image_data, std::vector<float> &mean, std::vector<float> &data);

private:
    void *mp_pred_hnd = NULL;
    int m_width;
    int m_height;
    int m_channels;
    std::vector<float> m_img_data;
};

#endif //DMS_MXNETPRED_H_H
