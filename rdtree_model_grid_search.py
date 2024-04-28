import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report
from joblib import dump, load
from collections import Counter
import time
import numpy as np
import argparse

def main(path, winsize):
    # 粗计时
    start_time = time.perf_counter()
    # 数据加载
    dataset = load(path + '/dataset/dataset_' + str(winsize) + '.joblib')
    # 输出到文件的目录
    output_dir = path + '/train_reports/tree_' + str(winsize)
    os.makedirs(output_dir, exist_ok=True)
    # 初始化randomtree
    rf = RandomForestClassifier(random_state=24)
    # #划分训练集和测试集
    # X_train, X_test, y_train, y_test = train_test_split(
    #     [item[0] for item in dataset],
    #     [item[1] for item in dataset],
    #     test_size=0.3, shuffle=True
    # )
    # 需要过滤数据集里过多的重复
    # 创建字典来统计每种特征组合及其标签的出现次数
    feature_count = Counter()
    # 统计特征出现频率
    for features, label in dataset:
        feature_tuple = (tuple(features), label)  # 将特征列表和标签转换成元组，作为字典的键
        feature_count[feature_tuple] += 1
    # 设置阈值，例如最多保留10次
    threshold = 10
    # 过滤数据集
    filtered_dataset = [item for item in dataset if feature_count[(tuple(item[0]), item[1])] <= threshold]
    # 确保数据集不为空
    if not filtered_dataset:
        raise ValueError("Filtered dataset is empty.")
    # 输出新数据集大小
    print(f"Original dataset size: {len(dataset)}")
    print(f"Filtered dataset size: {len(filtered_dataset)}")
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        [item[0] for item in filtered_dataset],
        [item[1] for item in filtered_dataset],
        test_size=0.3, shuffle=True
    )
    # 定义要尝试的参数范围
    parameter_space = {
        'n_estimators': [10, 20, 30, 50],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [5, 10, 20],
        'bootstrap': [True],
        'max_features': ['sqrt']
    }
    # 创建GridSearchCV对象
    clf = GridSearchCV(rf, parameter_space, n_jobs=-1, cv=3, scoring='accuracy', return_train_score=True)
    clf.fit(X_train, y_train)
    # 将最佳参数输出到文件
    with open(output_dir + '/best_parameters.txt', 'w') as file:
        file.write("Best parameters found:\n")
        for param, value in clf.best_params_.items():
            file.write(f"{param}: {value}\n")
    # 输出在测试集上的性能
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    df_report = pd.DataFrame(report).transpose()
    df_report.to_csv(output_dir + '/classification_report.csv')
    # 导出模型
    dump(clf.best_estimator_, output_dir + '/rdtree_best_model.joblib')
    # 将所有参数组合的性能得分保存到CSV文件
    df_cv_results = pd.DataFrame(clf.cv_results_)
    df_cv_results.to_csv(output_dir + '/gridsearch_cv_results.csv')
    # 在程序结束时记录时间
    end_time = time.perf_counter()
    # 计算执行时间
    execution_time = end_time - start_time
    # 打印并将执行时间写入文件
    with open(output_dir + '/timecount.txt', 'w') as file:
        runtime_message = f"Execution time with high precision: {execution_time:.2f} seconds"
        file.write(runtime_message)



# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description="Process the specified files with given parameters.")
# 添加命令行参数
parser.add_argument('--path', type=str, help='The directory path where files are located')
parser.add_argument('--winsize', type=int, help='Window size to use for processing')
# 解析命令行参数
args = parser.parse_args()
# 调用 main 函数并传入解析后的参数
main(args.path, args.winsize)