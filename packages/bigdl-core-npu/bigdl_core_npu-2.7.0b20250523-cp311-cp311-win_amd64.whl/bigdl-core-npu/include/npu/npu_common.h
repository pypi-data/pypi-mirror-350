//
// Copyright 2016 The BigDL Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

#pragma once

#include <string>
#include <vector>
#include <sstream>
#include <chrono>

#ifdef __linux__
#define EXPORT_API extern "C"
#else
#define EXPORT_API extern "C" __declspec(dllexport)
#endif


struct common_params {
    int32_t n_predict             =    -1; // new tokens to predict
    char* model                = ""; // model path                                                    // NOLINT
    std::string prompt               = "";                                                                  // NOLINT
    std::string prompt_file          = ""; // store the external prompt file name                           // NOLINT

    std::string cache_type_k = "f16"; // KV cache data type for the K
    std::string cache_type_v = "f16"; // KV cache data type for the V
};

struct npu_model_params {
    int32_t kv_len;
    int32_t max_prompt_len;
    int32_t num_head;
    int32_t head_dim;
    int32_t num_layers; 
    int32_t vocab_size;
    int32_t hidden_size;
    int32_t intermediate_size;
    int32_t group_size;
    int32_t fused_layers_num;
    int32_t fused_layers;
    int32_t weight_num;
    int32_t weight_idx;
    int32_t n_splits_linear;
    int32_t n_splits_down_proj;
    int32_t max_position_embeddings;
    bool embedding_post;
    std::string model_dir;
    std::string model_weight_dir;
    std::string model_name;
    std::string prefill_layer_blob_name;
    std::string lmhead_blob_name;
    std::string embedding_post_prefill_blob_name;
    std::string embedding_post_blob_name;
    std::string prefill_layer_ir_name;
    std::string lmhead_ir_name;
    std::string embedding_post_prefill_ir_name;
    std::string embedding_post_ir_name;
    std::string config;
    std::string low_bit;
    std::string lm_head_low_bit;
    bool const_parameter;
    std::string model_type;
    bool transpose_value_cache;
    bool qkv_bias;
    bool use_prefill_sdp;
    bool cos_sin_input;
    bool use_level_zero;
};

struct tokenizer_params {
    std::string tokenizer_file;
    int32_t bos_token_id;
    std::vector<int32_t> eos_token_id;
};

struct npu_generation_params {
    // may add more later when dealing with more cases
    float repetition_penalty;
    int32_t max_new_token;
};

struct llm_perf_data {
    std::chrono::time_point<std::chrono::high_resolution_clock> t_start;
    double t_load_ms;
    double t_p_eval_ms;
    double t_eval_ms;
    uint32_t n_p_eval;
    uint32_t n_eval;
};

#ifndef BASE64_H
#define BASE64_H

namespace base64 {
    std::string encode(const std::string &data);
    std::string decode(const std::string &data);
}

#endif // BASE64_H to encode and decode

#ifdef __cplusplus
extern "C" {
#endif

#ifdef __cplusplus
}
#endif