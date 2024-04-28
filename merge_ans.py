import pandas as pd
import os

def merge_posterior_ans_files(directory):
    # 定义基础文件路径
    posterior_file_path = os.path.join(directory, 'sample1.posterior')
    ans_files = ['sample1.ans', 'sample2.ans', 'sample3.ans', 'sample4.ans']

    # 读取 posterior 文件，跳过第一行，只保留前两列
    df_posterior = pd.read_csv(posterior_file_path, sep='\t', skiprows=1, usecols=[0, 1], names=['chrome', 'position'])

    # 合并 ans 文件
    for i, ans_file in enumerate(ans_files):
        ans_file_path = os.path.join(directory, ans_file)
        df_ans = pd.read_csv(ans_file_path, header=None, names=[f'sam{i+1}'])
        df_posterior = pd.concat([df_posterior, df_ans], axis=1)

    # 输出结果到新文件
    output_file_path = os.path.join(directory, 'merged_ans.csv')
    df_posterior.to_csv(output_file_path, index=False)

# 调用函数处理文件
directory = r'E:/毕业设计/ancestryhmm'
merge_posterior_ans_files(directory)