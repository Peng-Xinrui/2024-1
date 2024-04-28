import pandas as pd

# 读取CSV文件
file_path = 'E:/毕业设计/ancestryhmm/merged_ans.csv'
data = pd.read_csv(file_path)

# 按染色体分组并保存
for chromosome, group in data.groupby('chrome'):
    # 创建新的文件名
    new_file_path = f'E:/毕业设计/ancestryhmm/chrome_{chromosome}_ans.csv'

    # 去掉代表染色体的列
    group = group.drop('chrome', axis=1)

    # 重新设置剩余列的列名
    group.columns = ['Position', 'sam0', 'sam1', 'sam2', 'sam3']

    # 保存文件
    group.to_csv(new_file_path, index=False)


