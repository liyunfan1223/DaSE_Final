# 数据合并
import pandas as pd
import numpy as np

df_list = []
pagestart = 1
pageend = 500
for i in range(pagestart, pageend + 1):
    with open('raw_data/steam_info/crawled_info%s.csv' % str(i), 'r', encoding='utf-8') as file:
        df_list.append(pd.read_csv(file))
df = pd.concat(df_list)

print(df)

# rank = np.asarray(rank).reshape(len(rank), 1)
# print(type(rank))


df.to_csv('data/steam&meta_info.csv', index = 0, encoding='utf-8-sig')
