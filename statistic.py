# 统计绘图
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.datasets import imdb

def dataReader(filepath):
    with open(filepath,'r',encoding='utf-8') as f:
        data = pd.read_csv(f)
    print("数据加载完成。数据长度为 {} 。".format(len(data)))
    return data, len(data)

def getText(data):
    return data['reviewList']

def dataReader_imdb():
    (train_x, train_y), (test_x, test_y)= imdb.load_data()
    text = []
    for i in train_x:
        st = ''
        for j in i:
            st += str(j) + ' '
        text.append(st)
    return text, len(text)

def createDict(data): # data是一个文本Series
    Dict = {}
    sents = data
    for sent in sents:
        words = sent.split()
        for word in words:
            if word in Dict:
                Dict[word] += 1
            else:
                Dict[word] = 1
    sorted_keys = sorted(Dict.keys(), key = lambda x: Dict[x], reverse=True)
    sorted_Dict = {key : Dict[key] for key in sorted_keys}
    print("字典已生成并排序。共包含 {} 个单词。".format(len(sorted_Dict)))
    return sorted_Dict

def generate_length(data, ax, tot, label):
    count = np.zeros(2000)
    for line in data:
        Len = len(line.split())
        if Len < 2000:
            count[Len] += 1
    x = np.arange(5, 2000)
    count /= tot
    ax.bar(x, count[5:], label = label)

def generate_length_sum(data, ax, tot, label, color):
    count = np.zeros(800)
    for line in data:
        Len = len(line.split())
        if Len < 800:
            count[Len] += 1
    x = np.arange(5, 800)
    count /= tot
    index = 0
    quantile = 0
    for i in range(1, 800):
        count[i] += count[i - 1]
        if index == 0 and count[i] >= 0.9:
            index = i
            quantile = count[i]
    print(index, quantile)
    plt.hlines(0.9, 0, index, colors=color, linestyles="dashed")
    plt.vlines(index, -0.1, 0.9, colors=color, linestyles="dashed")
    plt.text(index, 0.92, (index, 0.9), color = 'black', fontsize = 14)
    ax.plot(x, count[5:], label = label)

def generate_frequency(Dict, ax, tot, label, color):
    keys = list(Dict.keys())
    count = np.zeros(10001)
    print(tot)
    for key in keys:
        freq = int(Dict[key] / tot * 10000) + 1
        if freq <= 10000:
            count[freq] += 1
    
    for i in range(1, 10001):
        count[i] += count[i - 1]

    count /= count[10000]
    index = 0
    for i in range(1, 10001):
        if index == 0 and count[i] >= 0.9:
            index = i / 100
    plt.hlines(0.9, 0, index, colors=color, linestyles="dashed")
    plt.vlines(index, -0.1, 0.9, colors=color, linestyles="dashed")
    plt.text(index, 0.92, (index, 0.9), color = 'black', fontsize = 14)
    x = np.arange(10001, dtype = 'float64')
    print(x)
    x /= 100
    ax.plot(x, count, label = label)

def setPltParams():
    plt.style.use('seaborn')
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False
    
def plt1(filepath):
    setPltParams()
    fig, ax = plt.subplots(figsize=(14, 7))
    text, tot = dataReader_imdb()
    Dict = createDict(text)
    generate_length(text, ax, tot, 'imdb')

    data, tot = dataReader(filepath)
    text = getText(data)
    Dict = createDict(text)
    generate_length(text, ax, tot, 'metacritic')

    ax.set_title("句子长度频数统计图")
    ax.set_xlabel("句子长度")
    ax.set_ylabel("频数")
    ax.set_xlim((2,2000))
    # ax.set_ylim((-0.02,1.05))
    
    plt.legend()
    plt.savefig('plt/句子长度频数统计图_f.png')
    plt.show()

def plt2(filepath):
    setPltParams()
    fig, ax = plt.subplots(figsize=(14, 7))
    text, tot = dataReader_imdb()
    Dict = createDict(text)
    generate_length_sum(text, ax, tot, 'imdb','r')

    data, tot = dataReader(filepath)
    text = getText(data)
    Dict = createDict(text)
    generate_length_sum(text, ax, tot, 'metacritic','c')

    ax.set_title("句子长度频数累积统计图")
    ax.set_xlabel("句子长度")
    ax.set_ylabel("频数")
    ax.set_xlim((2,800))
    ax.set_ylim((0, 1.05))
    plt.legend()
    plt.savefig('plt/句子长度频数累积统计图.png')
    plt.show()

def plt3(filepath):
    setPltParams()
    fig, ax = plt.subplots(figsize=(14, 7))

    text, tot = dataReader_imdb()
    Dict = createDict(text)
    generate_frequency(Dict, ax, tot, 'imdb','r')

    data, tot = dataReader(filepath)
    text = getText(data)
    Dict = createDict(text)
    generate_frequency(Dict, ax, tot, 'metacritic','c')
    
    ax.set_xlim(-0.002, 0.25)
    ax.set_ylim(0, 1)
    ax.set_title("单词频率累积统计图")
    ax.set_ylabel("累积单词比例")
    ax.set_xlabel("词频(%)")
    plt.legend(loc = 'lower right')
    plt.savefig('plt/单词频数累积统计图.png')
    plt.show()

if __name__ == '__main__':
    filepath = 'data/c_total.csv'
    data, tot = dataReader(filepath)
    print(data.describe())
    plt1(filepath)
    # plt2(filepath)
    # plt3(filepath)