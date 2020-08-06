#!/usr/bin/env bash
bert-base-serving-start \
    -model_dir '/home/admin/EA-CKGQA/NER/output/New_Model/' \
    -bert_model_dir '/home/admin/EA-CKGQA/NER/chinese_L-12_H-768_A-12'\
    -model_pb_dir '/home/admin/EA-CKGQA/NER/output/pd_model/'\
    -mode NER\
    -port 5555\
    -port_out 5556\ &