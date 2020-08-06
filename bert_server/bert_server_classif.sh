export BERT_BASE_DIR=/home/zhangqian/opt/jupyterhub/home/admin/EA-CKGQA/NER/chinese_L-12_H-768_A-12
export TRAINED_CLASSIFIER=./output
export EXP_NAME=mobile
sudo bert-base-serving-start \
    -model_dir $TRAINED_CLASSIFIER/$EXP_NAME \
    -bert_model_dir $BERT_BASE_DIR \
    -model_pb_dir $TRAINED_CLASSIFIER/$EXP_NAME \
    -mode CLASS \
    -max_seq_len 128 \
    -port 5559 \
    -port_out 5560 \
    -device_map 1  &