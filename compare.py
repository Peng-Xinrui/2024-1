import pandas as pd
import matplotlib.pyplot as plt


def calculate_accuracy_and_distribution(file1_path, file2_path):
    # 读取文件
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # 设定列名
    df1.columns = ['Position', 'sam0', 'sam1', 'sam2', 'sam3']
    df2.columns = ['Position', 'sam0', 'sam1', 'sam2', 'sam3']

    # 检查和对齐位置
    if not df1['Position'].equals(df2['Position']):
        raise ValueError("位置信息不匹配。请检查两个文件的位置列。"+str(file1_path))

    # 计算每个样本的准确率和状态分布
    accuracies = {}
    distributions = {}
    for col in ['sam0', 'sam1', 'sam2', 'sam3']:
        accuracies[col] = (df1[col] == df2[col]).mean()
        dist1 = df1[col].value_counts(normalize=True).sort_index()
        dist2 = df2[col].value_counts(normalize=True).sort_index()
        distributions[col] = (dist1, dist2)

    return accuracies, distributions


def plot_and_save_pie_charts(distributions, chromosome):
    for sample, dist in distributions.items():
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))

        # File 1 Pie Chart
        axs[0].pie(dist[0].values, labels=dist[0].index, autopct='%1.1f%%', startangle=90)
        axs[0].set_title(f'File 1 - {sample}')

        # File 2 Pie Chart
        axs[1].pie(dist[1].values, labels=dist[1].index, autopct='%1.1f%%', startangle=90)
        axs[1].set_title(f'File 2 - {sample}')

        plt.suptitle(f'State Distribution Comparison for {sample} - Chromosome {chromosome}')
        plt.savefig(f'E:/毕业设计/ancestryhmm/chrome_{chromosome}_{sample}_pie_chart.svg')
        plt.close()


# 创建一个空DataFrame来收集所有准确率数据
accuracy_df = pd.DataFrame()

# 主循环
for ind in [1, 2, 3, 4, 5, 6, 8,  10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
    file1_path = f'E:/毕业设计/ancestryhmm/chrome_{ind}_ans.csv'
    file2_path = f'E:/毕业设计/ancestryhmm/mlp_results_{ind}.csv'
    accuracies, distributions = calculate_accuracy_and_distribution(file1_path, file2_path)

    # 将当前染色体的准确率添加到DataFrame
    accuracy_df = pd.concat([accuracy_df, pd.DataFrame(accuracies, index=[f'Chromosome {ind}'])])

    plot_and_save_pie_charts(distributions, ind)

# 保存准确率数据到CSV文件
accuracy_df.to_csv('E:/毕业设计/ancestryhmm/accuracy_chrome_22.csv')
