# 结合游戏数据带入逻辑回归模型
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

with open('datasets/combined.csv','r',encoding='utf-8-sig')as f:
    data = pd.read_csv(f)

# X = data[['price', 'param1', 'param2', 'criticScore']]
X = data[['param1','param2','price','criticScore']]
Y = data['status']

X = np.asarray(X)
Y = np.asarray(Y)

print(X)

print(Y)

train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size = 0.1, random_state = 242)

model = LogisticRegression()
model.fit(train_x, train_y)

pred_y = model.predict(test_x)

print(pred_y)

pred_y2 = []
for line in test_x:
    p1 = line[0]
    p2 = line[1]
    pred_y2.append(1 if p2 > p1 else 0)

score = accuracy_score(pred_y2, test_y)

print('仅根据文本预测的准确率: {} %'.format(score * 100))

score = accuracy_score(pred_y, test_y)

print('结合评分和定价后的准确率: {} %'.format(score * 100))

