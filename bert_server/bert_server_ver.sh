#!/usr/bin/env bash
sudo bert-serving-start -model_dir "/home/zhangqian/opt/jupyterhub/home/admin/EA-CKGQA/NER/chinese_L-12_H-768_A-12" -num_worker=1 -port 5557 -port_out 5558 &