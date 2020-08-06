#!/usr/bin/env bash
# 分类模型导出pd模型
export BERT_BASE_DIR=/home/admin/EA-CKGQA/NER/chinese_L-12_H-768_A-12 #训练模型时使用的预训练语言模型所在路径
export TRAINED_CLASSIFIER=./output #训练好的模型输出的路径
export EXP_NAME=mobile #训练后保存的模型命名

python freeze_graph.py \
    -bert_model_dir $BERT_BASE_DIR \
    -model_dir $TRAINED_CLASSIFIER/$EXP_NAME \
    -max_seq_len 128 #注意，这里的max_seq_len应与训练的脚本train.sh设置的max_seq_length参数值保持一致