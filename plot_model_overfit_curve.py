import os
from sklearn.model_selection import train_test_split
from joblib import load
import numpy as np
import argparse
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

def main(datapath,modelpath,outputdir,winsize):
    dataset = load(datapath+'/dataset_'+str(winsize)+'.joblib')
    clf=load(modelpath+'/mlp_model.joblib')
    # 输出到文件的目录
    output_dir = outputdir
    os.makedirs(output_dir, exist_ok=True)
    #划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        [item[0] for item in dataset],
        [item[1] for item in dataset],
        test_size=0.3, shuffle=True
    )
    train_sizes, train_scores, test_scores = learning_curve(
        clf, X_train, y_train, cv=3,
        train_sizes=np.linspace(0.1, 1.0, 5)
    )
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.figure()
    plt.title("Learning Curve for MLP Classifier")
    plt.xlabel("Training Data Size")
    plt.ylabel("Accuracy")
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    plt.savefig(os.path.join(output_dir, 'learning_curve.png'))
    plt.savefig(os.path.join(output_dir, 'learning_curve.svg'))
    plt.show()


# # 创建 ArgumentParser 对象
# parser = argparse.ArgumentParser(description="Process the specified files with given parameters.")
# # 添加命令行参数
# parser.add_argument('--datapath', type=str, help='The directory path where dataset files are located')
# parser.add_argument('--modelpath', type=str, help='The directory path where model files are located')
# parser.add_argument('--outputdir', type=str, help='The directory path where output files should located')
# parser.add_argument('--winsize', type=int, help='Window size to use for processing')
# # 解析命令行参数
# args = parser.parse_args()
# # 调用 main 函数并传入解析后的参数
# main(args.datapath,args.modelpath, args.outputdir, args.winsize)
datapath='D:/1Semester/1ML/ML20334030/simdata/restart/simtest/55/dataset'
modelpath='D:/1Semester/1ML/ML20334030/simdata/restart/train_reports_/mlp_50'
outputdir='D:/1Semester/1ML/ML20334030/simdata/restart/train_reports_/mlp_50'
winsize=50
main(datapath,modelpath, outputdir,winsize)





















