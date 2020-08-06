#!/usr/bin/env bash
bert-base-serving-start \
    -model_dir '/home/admin/EA-CKGQA/NER/POETRY_New_Model/' \
    -bert_model_dir '/home/admin/EA-CKGQA/NER/chinese_L-12_H-768_A-12'\
    -mode NER\
    -port 5555\
    -port_out 5556\ &