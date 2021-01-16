# 数据合并
import pandas as pd
import numpy as np

if __name__ == '__main__':
    start = 1
    end = 100
    dfList = []
    for i in range(start, end + 1):
        print("正在合并第 {} 项... 共 {} 项".format(i, end))
        path = 'raw_data/game_reviews%s.csv' % str(i)
        with open(path, 'r', encoding='utf-8') as file:
            df = pd.read_csv(file)
            dfList.append(df)

    new_df = pd.concat(dfList)
    new_df.to_csv('data/data_reviews.csv', index = 0, encoding = 'utf-8-sig')