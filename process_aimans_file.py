import os
import argparse
###
#将模拟数据的*_ancestry_hap1.txt，*_ancestry_hap2.txt根据AIMS_sort提出aims位置并对照转化成祖先情况，id就是第几个个体
#AIMS_sort是用get_aims.sh简单处理的aims位置，按顺序排列了
#0即原本的'b'，1即原本的'm'，由于模拟数据无缺失位点且单个文件都是单倍的，因此这里没有代表缺失的N和代表杂合的2
def process_aimans_files(path,id):
    aims_file=path+'/AIMS_sort'
    ances_path_1=path+'/hybrid_genomes/'+str(id)+'_ancestry_hap1.txt'
    ances_path_2=path+'/hybrid_genomes/'+str(id)+'_ancestry_hap2.txt'
    ances_file_1=open(ances_path_1,'r')
    first_line =ances_file_1.readline()
    ances_file_2=open(ances_path_2,'r')
    first_line =ances_file_2.readline()
    os.makedirs(path+'/hybrid_genomes_ans', exist_ok=True)
    aimans_path=path+'/hybrid_genomes_ans/'+str(id)+'_ancestry_aimans.txt'
    aimans_file=open(aimans_path, 'w')
    i=0
    #遍历AIMS里的位置
    with open(aims_file, 'r') as file:
        for line in file:
            pos=int(line.strip())
            nowances_1='N'
            nowances_2='N'
            while(i<pos):
                nowances_1=ances_file_1.read(1)
                nowances_2=ances_file_2.read(1)
                i=i+1
            #读到了pos的位置
            if((nowances_1=='b') and (nowances_2=='b')):
                #bb
                aimans_file.write(str(0))
            elif((nowances_1=='m')and (nowances_2=='m')):
                #mm
                aimans_file.write(str(1))
            elif(((nowances_1=='b') and (nowances_2=='m')) or ((nowances_1=='m')and (nowances_2=='b'))):
                #杂合
                aimans_file.write(str(2))
            else:
                aimans_file.write('N')
    ances_file_1.close()
    ances_file_2.close()
    aimans_file.close()

def main(path):
    for ind in range(10):
        process_aimans_files(path,ind)

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description="Process the specified files with given parameters.")
# 添加命令行参数
parser.add_argument('--path', type=str, help='The directory path where files are located')
# 解析命令行参数
args = parser.parse_args()
# 调用 main 函数并传入解析后的参数
main(args.path)

