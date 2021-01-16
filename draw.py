# 绘制实验结果
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# 画四条折线 分别表示不同数据集下的每种训练方法的正确率
# [0,1,2,3]分别表示：[Tfidf, LSTM, Dense, CNN]
data1 = [59.46, 60.17, 58.54, 60.20] # 短文本大量
data2 = [89.28, 89.12, 89.08, 90.55] # imdb电影评论
data3 = [87.73, 75.37, 68.65, 84.01] # 长文本少量
data4 = [97.87, 95.56, 97.52, 98.40] # 长文本大量

plt.style.use('seaborn')
matplotlib.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
fig, ax = plt.subplots(figsize = (20, 10))
X = np.arange(4)
labels = ['Tfidf', 'LSTM', 'Dense', 'CNN']
ax.plot(X, data1, 'o--', label = '短文本 大量')
ax.plot(X, data2, 'o--', label = 'imdb电影评论')
ax.plot(X, data3, 'o--', label = '长文本 少量')
ax.plot(X, data4, 'o--', label = '长文本 大量')

ax.set_xticks(X)
ax.set_xticklabels(labels, fontsize = 16)
ax.set_ylim((40,102))
ax.set_xlim((-0.2, 3.5))
ax.set_ylabel("准确率")
ax.set_xlabel("模型")
ax.set_title("不同数据集在不同模型下的表现情况")
plt.legend()
plt.savefig('plt/不同数据集在不同模型下的表现情况4.png')
plt.show()