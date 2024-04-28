import os
import sys
import pandas as pd
import math
from collections import deque
from joblib import dump
from joblib import load
import numpy as np
###
#path,窗口大小winsize都是全局的
winsize=100
path='E:/毕业设计/ancestryhmm/example_chromosome_panel'
model_path = 'E:/毕业设计/SIM1000/82/train_reports'
mlp_model = load(model_path+'/mlp_'+str(winsize)+'/mlp_model.joblib')
# rdt_model = load(model_path+'/rdtree_50/rdtree_best_model.joblib')
# path='/public3/group_crf/home/b20pengxr23/msgsim/MSGsimulator/example_simulation_files_results/example_simulation_results_2'
###
def make_pre_win(leftnan,midlist,rightnan):
    window_now=([-1]*leftnan)+(midlist)+([-1]*rightnan)
    return np.array(window_now).reshape(1, -1)
#将state_i.panel代表的N个样本状态做成窗口,预测并输出结果的表格
def predict_panel(L,state_file,chrome):
    #先初始化按列提取样本的状态
    pos_list = []
    mlp_results=pd.DataFrame()
    # rdtree_results = pd.DataFrame()
    #4个sample
    num_samples = 4
    samples_states = [[] for _ in range(num_samples)]
    # 读取文件来填充数据
    with open(state_file, 'r') as file:
        for line in file:
            row = line.strip().split('\t')
            pos_list.append(int(row[0]))  # 位置
            # 读取每个样本的状态
            for i in range(num_samples):
                samples_states[i].append(int(row[i + 1]))  # 第i个样本的状态
    mlp_results['Position'] = pos_list[:]
    # rdtree_results['Position'] = pos_list[:]
    # 对sam_i进行处理
    for i, states in enumerate(samples_states):
        # 前面窗口补前面的缺失序列-1
        queue_ans = deque(maxlen=L)
        pre_mlp = []
        # pre_rdtree = []
        zero_num = math.floor(L / 2)
        rest_num = L - zero_num
        # 半个窗口的内容入队
        j=0
        length=len(states)
        while(j<rest_num):
            currentans=states[j]
            queue_ans.append(currentans)
            j=j+1
        while (zero_num >= 1):
            window_now = [-1] * zero_num
            window_now.extend(list(queue_ans))
            # 转换为Numpy数组并调整形状
            trait_array = np.array(window_now).reshape(1, -1)
            mlp_prediction = mlp_model.predict(trait_array)
            mlp_prediction=mlp_prediction[0]
            # rdtree_prediction=rdt_model.predict_proba(trait_array)
            pre_mlp.append(mlp_prediction)
            # pre_rdtree.append(rdtree_prediction)
            zero_num = zero_num - 1
            currentans=states[j]
            queue_ans.append(currentans)
            j=j+1
        # 然后是中间的窗口
        while (1):
            if (j>=length):
                queue_ans.pop()
                break
            window_now = (list(queue_ans))
            # 转换为Numpy数组并调整形状
            trait_array = np.array(window_now).reshape(1, -1)
            mlp_prediction = mlp_model.predict(trait_array)
            mlp_prediction = mlp_prediction[0]
            # rdtree_prediction = rdt_model.predict_proba(trait_array)
            pre_mlp.append(mlp_prediction)
            # pre_rdtree.append(rdtree_prediction)
            currentans = states[j]
            queue_ans.append(currentans)
            j=j+1
        # 然后是后面的窗口在后面补缺失序列'N'
        zero_num = math.floor(L / 2) - 1
        zero_num_now = 1
        while (zero_num_now <= zero_num):
            zero_now = [-1] * zero_num_now
            window_now = (list(queue_ans))
            window_now.extend(zero_now)
            # 转换为Numpy数组并调整形状
            trait_array = np.array(window_now).reshape(1, -1)
            mlp_prediction = mlp_model.predict(trait_array)
            mlp_prediction = mlp_prediction[0]
            # rdtree_prediction = rdt_model.predict_proba(trait_array)
            pre_mlp.append(mlp_prediction)
            # pre_rdtree.append(rdtree_prediction)
            queue_ans.popleft()
            zero_num_now = zero_num_now + 1
        trait_array=make_pre_win(0,[states[-1]],winsize-1)
        mlp_prediction = mlp_model.predict(trait_array)
        mlp_prediction = mlp_prediction[0]
        # rdtree_prediction = rdt_model.predict_proba(trait_array)
        pre_mlp.append(mlp_prediction)
        # pre_rdtree.append(rdtree_prediction)
        mlp_results['sam'+str(i)]=pre_mlp
        # rdtree_results['sam' + str(i)] = pre_rdtree
    mlp_results.to_csv(path+'/mlp_results_'+str(chrome)+'.csv', index=False)  # 保存MLP模型的结果到CSV
    # rdtree_results.to_csv('rdtree_results_'+str(chrome)+'.csv', index=False)  # 保存Random Forest模型的结果到CSV


###主函数部分
for ind in [1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]:
    predict_panel(winsize,path+'/state_'+str(ind)+'.panel',ind)


