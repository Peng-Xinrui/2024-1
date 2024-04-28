import os
import numpy as np
import math
from collections import deque
from joblib import dump
from joblib import load
import argparse


#训练需要把祖先情况变成数字映射
def make_a_train(windowsites):
    convert_map = {'N': -1,'0': 0, '1': 1, '2': 2}
    converted_win = [convert_map[elem] for elem in windowsites]
    window_L=math.floor(len(windowsites)/2)
    return [converted_win,converted_win[window_L]]
#填充出完整的窗口
def make_full_win(isleft,midlist,isright,winsize):
    len_now=len(midlist)
    fill_num=winsize-len_now
    if(isleft):
        #左边填充N
        window_now=(['N']*fill_num)+(midlist)
    elif(isright):
        #右边填充N
        window_now = (midlist)+ (['N'] * fill_num)
    else:
        window_now = (midlist)
    return window_now

#将用process_aimans_files的aims做成窗口,返回可以用来训练的dataset_winsize
def make_wins(id,path,winsize):
    aimans_path=path+'/hybrid_genomes_ans/'+str(id)+'_ancestry_aimans.txt'
    os.makedirs(path + '/hybrid_genomes_ans', exist_ok=True)
    aimans_file=open(aimans_path, 'r')
    #用来放aims的滑动窗，大小为winsize
    queue_ans = deque(maxlen=winsize)
    #对于该个体生成的数据集保存在
    dataset_now = []
    #让第一个aim成为窗口中间，则前面有zero_num个‘N’
    zero_num = math.floor(winsize/ 2)
    rest_num = winsize - zero_num
    #半个窗口的内容入队形成第一个窗
    for i in range(rest_num):
        currentans = aimans_file.read(1)
        queue_ans.append(currentans)
    #开始的有缺失的窗口
    while (zero_num >= 1):
        window_now =make_full_win(True,list(queue_ans),False,winsize)
        dataset_now.append(make_a_train(window_now))
        zero_num = zero_num - 1
        currentans = aimans_file.read(1)
        queue_ans.append(currentans)
    #然后是中间的窗口
    while(1):
        if(currentans==''):
            #此时已经读到aimans.txt文件的结尾，并且最后一个''加入了队列
            queue_ans.pop()
            break
        window_now=(list(queue_ans))
        dataset_now.append(make_a_train(window_now))
        currentans=aimans_file.read(1)
        queue_ans.append(currentans)
    #让最后一个aim成为窗口中间，则后面有zero_num(或-1)个‘N’
    if(winsize%2==0):
        zero_num = math.floor(winsize / 2)-1
    else:
        zero_num = math.floor(winsize / 2)
    while (zero_num >= 1):
        window_now = make_full_win(False,list(queue_ans),True,winsize)
        dataset_now.append(make_a_train(window_now))
        queue_ans.popleft()
        zero_num = zero_num - 1
    aimans_file.close()
    return dataset_now

#对第i个个体的造数据全过程,结果输出为完整的dataset_winsize.joblib'
def train_one_ind(id,path,winsize):
    dataset=make_wins(id,path,winsize)
    os.makedirs(path + '/dataset', exist_ok=True)
    if(id>0):
        data=load(path + '/dataset/dataset_'+str(winsize)+'.joblib')
        data=data+dataset
        dump(data,path + '/dataset/dataset_'+str(winsize)+'.joblib')
    else:
        dump(dataset, path + '/dataset/dataset_'+str(winsize)+'.joblib')


def main(path, winsize):
    for ind in range(10):
        train_one_ind(ind,path,winsize)

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description="Process the specified files with given parameters.")
# 添加命令行参数
parser.add_argument('--path', type=str, help='The directory path where files are located')
parser.add_argument('--winsize', type=int, help='Window size to use for processing')
# 解析命令行参数
args = parser.parse_args()
# 调用 main 函数并传入解析后的参数
main(args.path, args.winsize)
###

