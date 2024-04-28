import pandas as pd
from scipy.stats import pearsonr

# 构造数据
data = {
    "Parental Ratio": [0.5, 0.6, 0.7, 0.8, 0.9],  # 亲本比例，数值化表示
    "Log Loss 10": [0.033783428, 0.034454718, 0.035846906, 0.038547205, 0.042103885],
    "Log Loss 20": [0.00886561, 0.010981698, 0.01353063, 0.017276315, 0.021704696],
    "Log Loss 30": [0.011084118, 0.008742281, 0.007022287, 0.006680303, 0.007291226],
    "Log Loss 50": [0.001907882, 0.001589594, 0.001172183, 0.001184952, 0.001407783],
    "Log Loss 100": [0.000217015, 0.000198327, 0.000112537, 0.0000886, 0.0000941],
    "Log Loss 200": [0.000128415, 0.000104792, 0.0000651, 0.0000282, 0.0000242]
}
#{'Log Loss 10': PearsonRResult(statistic=0.9606213588839997, pvalue=0.009324872597126985), 'Log Loss 20': PearsonRResult(statistic=0.9882272401595746, pvalue=0.0015306745815251855), 'Log Loss 30': PearsonRResult(statistic=-0.8420263429618102, pvalue=0.07356012331517224), 'Log Loss 50': PearsonRResult(statistic=-0.722259683467819, pvalue=0.1681960059514609), 'Log Loss 100': PearsonRResult(statistic=-0.9237910698640716, pvalue=0.024964036205163416), 'Log Loss 200': PearsonRResult(statistic=-0.978101645005899, pvalue=0.003877210556175368)}

df = pd.DataFrame(data)

# 计算皮尔逊相关系数和p值
correlations = {col: pearsonr(df['Parental Ratio'], df[col]) for col in df.columns if 'Log Loss' in col}

print(correlations)
