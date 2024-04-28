import subprocess
import logging

# 设置日志记录
logging.basicConfig(filename='run_scripts_0425.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
pathlist_1=['E:/毕业设计/SIM10','E:/毕业设计/SIM100','E:/毕业设计/SIM10000']
#转化成aimans文件
for path in pathlist_1:
        script='process_aimans_file.py'
        subprocess.run(['python', script, '--path', path], check=True)
#制造在不同的祖源比例模拟制造不同windize的数据集
for path in pathlist_1:
    for winsize in [10,20,30,50,100]:
        script='makedataset.py'
        try:
            logging.info(f'Starting {script}')
            subprocess.run(['python', script, '--path', path, '--winsize', str(winsize)], check=True)
            logging.info(f'Finished {script}')
        except subprocess.CalledProcessError as e:
            logging.error(f'Error occurred while running {script}: {e}')
#只在gen10000上进行训练gridsearch
path='E:/毕业设计/SIM10000'
scripts = [
    'mlp_model_grid_search.py','rdtree_model_grid_search.py'
]
for winsize in [10,20,30,50,100]:
    for script in scripts:
        try:
            logging.info(f'Starting {script}')
            subprocess.run(['python', script, '--path', path, '--winsize', str(winsize)], check=True)
            logging.info(f'Finished {script}')
        except subprocess.CalledProcessError as e:
            logging.error(f'Error occurred while running {script}: {e}')