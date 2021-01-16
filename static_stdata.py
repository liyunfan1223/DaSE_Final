# 统计绘图
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


with open('datasets/cleaned_data_info.csv', encoding='utf-8') as file:
    data = pd.read_csv(file)
# data = data[:5000]
print(data.describe())

def PLOT_date_price():
    X = data['publish_year'] + data['publish_month'] / 12 + data['publish_day'] / 365
    Y = data['price']
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(14, 7))
    matplotlib.rcParams['font.sans-serif']=['SimHei']

    plt.scatter(X, Y, s=np.sqrt(data['comments_total'] / 100), c=data['praise_rate_total'], alpha=.9, cmap=plt.get_cmap('Spectral'))

    ax.set_xlim((2004.5,2021.5))
    ax.set_ylim((-20, 450))
    x_major_locator=MultipleLocator(2)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.set_xlabel('年份')
    ax.set_ylabel('价格(￥)')
    plt.colorbar().set_label('好评率(%)')
    # plt.savefig('fig/scatter_date_price.png')
    plt.show()

def PLOT_date_praise_rate():
    X = data['publish_year'] + data['publish_month'] / 12 + data['publish_day'] / 365
    Y = data['praise_rate_total']
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(14, 7))
    matplotlib.rcParams['font.sans-serif']=['SimHei']

    ax.scatter(X, Y, s=15000/(data.index+200), c=data['praise_rate_total'], alpha=.95, cmap=plt.get_cmap('winter'))

    ax.set_xlim((2004.5,2021.5))
    ax.set_ylim((0, 101))
    x_major_locator=MultipleLocator(2)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.set_xlabel('年份')
    ax.set_ylabel('好评率(%)')
    # plt.savefig('fig/scatter_date_praise_rate.png')
    plt.show()

def PLOT_date_rate_price():
    y_price = []
    y_rate = []
    for i in range(2000, 2021):
        y_price.append(data.loc[data['publish_year'] == i]['price'].mean())
        y_rate.append(data.loc[data['publish_year'] == i]['praise_rate_total'].mean())
    x = np.arange(2000, 2021)
    print(plt.style.available)
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(14, 7))

    matplotlib.rcParams['font.sans-serif']=['SimHei']
    ax.plot(x, y_price, "v-", label = '平均价格')
    ax.plot(x, y_rate, "o--", label = '平均好评率')
    plt.legend()
    print(x)
    print(y_price)
    print(y_rate)
    ax.set_ylim((0, 101))
    ax.set_xlim((1999.8, 2021))
    ax.set_xlabel('年份')
    ax.set_ylabel('价格(￥)/好评率(%)')
    x_major_locator=MultipleLocator(2)
    ax.xaxis.set_major_locator(x_major_locator)
    # plt.savefig('fig/plot_date_rate_price.png')
    plt.show()

def PLOT_tags():
    frequency = {}
    for word in data['tag']:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    frequency = sorted(frequency.items(), key=lambda item:item[1], reverse=True)
    # frequency = sorted(frequency.items(),key = lambda x :x[1], reverse=True)#根据词频降序做排列输出一个元组
    x_label = []
    x = np.arange(8)
    y = []
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(20, 10))
    matplotlib.rcParams['font.sans-serif']=['SimHei']
    for i in range(8):
        x_label.append(frequency[i][0])
        y.append(frequency[i][1])
        ax.bar(i, frequency[i][1], facecolor='#ff9999', edgecolor='white')
    ax.set_xticklabels(x_label, fontsize = 8)
    ax.set_xticks(x)
    ax.set_ylabel('游戏数')
    # plt.savefig('fig/bar_tags.png')
    plt.show()

def plot_newtags_date():
    taglabel = ['角色扮演','冒险','动作','解谜','模拟','休闲','策略','第一人称射击']
    print(data)
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(20, 10))
    matplotlib.rcParams['font.sans-serif']=['SimHei']
    for tag in taglabel:
        x = np.arange(1980,2021)
        y = []
        for year in range(1980, 2021):
            nd = data.loc[data['publish_year'] == year].loc[data['tag'] == tag]
            y.append(len(nd))
        ax.plot(x, y, label = tag)
    plt.legend()
    plt.show()

def plot_player_date():
    print(data)
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(20, 10))
    matplotlib.rcParams['font.sans-serif']=['SimHei']
    for player in range(2):
        x = np.arange(2000,2021)
        y = []
        for year in range(2000, 2021):
            nd = data.loc[data['publish_year'] == year].loc[data['player'] == player]
            y.append(len(nd))
        ax.plot(x, y, label = str(player))
    plt.legend()
    plt.show()

def calc_pred(model, x):
    print(model.get_params())

def plot_two_scores():
    x = []
    y = []
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(20, 10))
    matplotlib.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    totrate = 0
    totscore = 0
    x = data['userScores'] * 10 + np.random.rand(len(data))
    y = data['criticScores'] + np.random.rand(len(data))
    yy = y[np.argsort(x)]
    yy = np.asarray(yy)
    xx = np.sort(x)
    X = xx.reshape(-1, 1)
    Y = yy.reshape(-1, 1)

    poly_reg = Pipeline([
        ("poly", PolynomialFeatures(degree=5)),
        ("std_scaler", StandardScaler()),
        ("lin_reg", LinearRegression())
    ])

    poly_reg.fit(X,yy)
    y_pred = poly_reg.predict(X)
    print(y_pred)
    print(yy)
    # plt.plot(xx, y_pred,c="black",label="拟合曲线")
    plt.plot(xx, y_pred + 4,c="red")
    plt.plot(xx, y_pred - 4,c="blue")

    XX = np.asarray(x)
    XX = XX.reshape(-1, 1)
    y_pred_sca = poly_reg.predict(XX)

    sca_x_1 = []
    sca_y_1 = []
    y_pp_1 = []
    idx_1 = []

    sca_x_2 = []
    sca_y_2 = []
    y_pp_2 = []
    idx_2 = []
    status = []
    for i in range(len(x)):
        nx = x[i]
        ny = y[i]
        y_pred_s = y_pred_sca[i]
        if y_pred_s - ny >=  999:
            sca_x_1.append(nx)
            sca_y_1.append(ny)
            y_pp_1.append(y_pred_s)
            idx_1.append(i)
            status.append(1)
        elif y_pred_s - ny <= -5 or y_pred_s - ny >= 5:
            sca_x_2.append(nx)
            sca_y_2.append(ny)
            y_pp_2.append(y_pred_s)
            idx_2.append(i)
            status.append(0)
        else:
            status.append(np.nan)
    # data['status'] = status
    # data.to_csv('data/tagged_total.csv',index=0,encoding='utf-8-sig')
    for i in range(len(x)):
        nx = x[i]
        ny = y[i]

    sca_x_2.append(x[0])
    sca_y_2.append(y_pred_sca[0])
    idx_2.append(1)
    y_pp_2.append(y_pred_sca[0])

    sca_x_1 = np.asarray(sca_x_1)
    sca_y_1 = np.asarray(sca_y_1)
    y_pp_1 = np.asarray(y_pp_1)
    idx_1 = np.asarray(idx_1)
    idx_1 = np.random.permutation(idx_1)
    sca_x_2 = np.asarray(sca_x_2)
    sca_y_2 = np.asarray(sca_y_2)
    y_pp_2 = np.asarray(y_pp_2)
    idx_2 = np.asarray(idx_2)
    idx_2 = np.random.permutation(idx_2)
    idx = np.arange(len(x))
    idx = np.random.permutation(idx)
    idx_1 = idx[:len(idx_1)]
    idx_2 = idx[-len(idx_2):]
    
    # plt.scatter(sca_x_1,sca_y_1,s= 10000 / (idx_1 + 200),c='b', alpha=.95, cmap=plt.get_cmap('viridis'))
    # plt.scatter(sca_x_2,sca_y_2,s= 10000 / (idx_2 + 200),c='r', alpha=.95, cmap=plt.get_cmap('viridis'))
    plt.scatter(sca_x_2,sca_y_2,s=60000/(idx_2+10000),c=np.sqrt(np.sqrt(np.sqrt(abs(sca_y_2 - y_pp_2)))), alpha=.9, cmap=plt.get_cmap('viridis'))
    
    ax.set_title('玩家评分与媒体评分关系图')
    ax.set_xlabel('玩家评分')
    ax.set_ylabel('媒体评分')
    plt.colorbar().set_label('比例',fontsize=20)
    plt.legend()
    plt.savefig('img/玩家评分与媒体评分关系图4.png')
    plt.show()

if __name__ == '__main__':
    # PLOT_date_price()
    # PLOT_date_praise_rate()
    # PLOT_date_rate_price()
    # PLOT_tags()
    # plot_newtags_date()
    # plot_player_date()
    plot_two_scores()