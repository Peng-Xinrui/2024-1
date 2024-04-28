import os
import csv

def split_panel_by_chromosome(input_file, base_path):
    # 创建存储文件的目录
    output_dir = os.path.join(base_path, 'example_chromosome_panel')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 创建一个字典来保存每个染色体的数据行
    chromosome_data = {}

    # 读取原始panel文件
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            chromosome = row[0]
            # 检查该染色体是否已在字典中
            if chromosome not in chromosome_data:
                chromosome_data[chromosome] = []
            # 添加当前行到对应的染色体列表中
            chromosome_data[chromosome].append(row)

    # 为每个染色体写入一个新的panel文件到指定的目录
    for chromosome, data in chromosome_data.items():
        # 计算行数
        num_lines = len(data)
        # 构建文件名，包含行数
        output_file = os.path.join(output_dir, f'example_{chromosome}.panel')
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(data)

# 定义文件路径和基础路径
input_path = "E:/毕业设计/ancestryhmm/example/example.panel"
base_path = "E:/毕业设计/ancestryhmm"

# 调用函数
split_panel_by_chromosome(input_path, base_path)

