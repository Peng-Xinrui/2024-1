import pandas as pd
import numpy as np
import os

def process_posterior_files(directory):
    # 遍历目录下的所有 .posterior 文件
    for filename in os.listdir(directory):
        if filename.endswith('.posterior'):
            # 读取文件
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path, sep='\t')

            # 初始化新列用于保存随机选取的状态
            df['random_state'] = np.nan

            # 列名映射到数字
            state_mapping = {'2,0': 0, '1,1': 2, '0,2': 1}

            # 遍历每行，基于概率随机选择状态
            for index, row in df.iterrows():
                probabilities = row[['2,0', '1,1', '0,2']].values
                # 检查概率是否包含NaN，如果是，则填充等概率
                if np.isnan(probabilities).any():
                    probabilities = np.array([1/3] * 3)
                else:
                    # 归一化概率，确保总和为1
                    probabilities /= probabilities.sum()

                states = np.array([0, 1, 2])  # 按概率列的顺序对应状态
                chosen_state = np.random.choice(states, p=probabilities)
                df.at[index, 'random_state'] = chosen_state

            # 转换 'random_state' 列为整数类型
            df['random_state'] = df['random_state'].astype(int)

            # 将结果输出到新文件
            output_filename = filename.replace('.posterior', '.ans')
            output_path = os.path.join(directory, output_filename)
            df['random_state'].to_csv(output_path, index=False, header=False)

# 调用函数处理文件
directory = r'E:/毕业设计/ancestryhmm'
process_posterior_files(directory)
