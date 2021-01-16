# 数据预处理

import numpy as np
import pandas as pd

def dataReader(filepath):
    with open(filepath,'r',encoding='utf-8') as f:
        data = pd.read_csv(f)
    return data

def processing(data):
    data = data.dropna()
    return data

def saveData(data, savepath):
    data.to_csv(savepath, encoding='utf-8-sig')

if __name__ == '__main__':
    filepath = 'data/processed_data_reviews.csv'
    savepath = 'data/processed_data_reviews.csv'
    data = dataReader(filepath)
    newData = processing(data)
    saveData(newData, savepath)