import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, log_loss, mean_squared_error, confusion_matrix
from joblib import load
from collections import Counter
import os

def evaluate_model(model_path, dataset_path, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 载入模型
    model = load(model_path)

    # 载入数据集
    data = load(dataset_path)
    X_test, y_test = zip(*[(item[0], item[1]) for item in data])
    # 创建字典来统计每种特征组合及其标签的出现次数
    feature_count = Counter()
    # 统计特征出现频率
    for features, label in data:
        feature_tuple = (tuple(features), label)  # 将特征列表和标签转换成元组，作为字典的键
        feature_count[feature_tuple] += 1
    # 设置阈值，例如最多保留10次
    threshold = 10
    # 过滤数据集
    filtered_dataset = [item for item in data if feature_count[(tuple(item[0]), item[1])] <= threshold]
    # 确保数据集不为空
    if not filtered_dataset:
        raise ValueError("Filtered dataset is empty.")
    # 输出新数据集大小
    print(f"Original dataset size: {len(data)}")
    print(f"Filtered dataset size: {len(filtered_dataset)}")
    X_test, y_test = zip(*[(item[0], item[1]) for item in filtered_dataset])
    # 进行预测
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)  # 获取所有类的概率

    # 计算评估指标
    accuracy = accuracy_score(y_test, y_pred)
    logloss = log_loss(y_test, y_prob)  # 注意这里使用完整的概率数组
    mse = mean_squared_error(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    error_count = conf_matrix.sum() - np.diag(conf_matrix).sum()
    # 保存评估指标到文件
    with open(os.path.join(output_dir, 'filledevaluation_results_'+str(gen)+'_winsize'+str(winsize)+'.txt'), "w") as file:
        file.write(f"Accuracy: {accuracy}\n")
        file.write(f"Log Loss: {logloss}\n")
        file.write(f"Mean Squared Error: {mse}\n")
        file.write("Confusion Matrix:\n")
        file.write(np.array2string(conf_matrix))
        file.write(str(error_count))

    print("Evaluation complete. Results saved to:", output_dir)

# 主程序
# 设置模型、数据集路径和输出目录
# model_id=82
# for winsize in [10,20,30,50,100,200]:
#     for data_id in [55,64,73,82,91]:
#         model_path = 'E:/毕业设计/SIM1000/'+str(model_id)+'/train_reports/tree_'+str(winsize)+'/rdtree_best_model.joblib'
#         dataset_path = 'E:/毕业设计/SIM1000/'+str(data_id)+'/dataset/dataset_'+str(winsize)+'.joblib'
# # dataset_path = 'D:/1Semester/1ML/ML20334030/simdata/restart/0dataset/dataset_'+str(winsize)+'.joblib'
#         output_dir = 'E:/毕业设计/SIM1000/partest'
#         os.makedirs(output_dir, exist_ok=True)
#         # 调用评估函数
#         evaluate_model(model_path, dataset_path, output_dir)
model_id=82
for winsize in [10,20,30,50,100]:
    for gen in [10,100,1000,10000]:
        model_path = 'E:/毕业设计/SIM1000/'+str(model_id)+'/train_reports/tree_'+str(winsize)+'/rdtree_best_model.joblib'
        dataset_path = 'E:/毕业设计/SIM'+str(gen)+'/dataset/dataset_'+str(winsize)+'.joblib'
# dataset_path = 'D:/1Semester/1ML/ML20334030/simdata/restart/0dataset/dataset_'+str(winsize)+'.joblib'
        output_dir = 'E:/毕业设计/SIM1000/gentest'
        os.makedirs(output_dir, exist_ok=True)
        # 调用评估函数
        evaluate_model(model_path, dataset_path, output_dir)


