# 数据清洗
import numpy as np
import pandas as pd

# 清洗方式：去除评论中出现最多的50个单词，以及只出现了一次的单词
# 只保留长度大于30的评论

def dataReader(filepath):
    with open(filepath,'r',encoding='utf-8') as f:
        data = pd.read_csv(f)
    print("数据加载完成。数据长度为 {} 。".format(len(data)))
    return data

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

def getStopWords(Dict):
    stopWords = []
    keys = list(Dict.keys())
    for i in range(20):
        stopWords.append(keys[i])
    for key in keys:
        if Dict[key] == 1:
            stopWords.append(key)
    stopWords = set(stopWords)
    print("停用词整理完毕。共 {} 个。".format(len(stopWords)))
    return stopWords

def dataCleaner(data, stopWords):
    cleanedData = data
    newReview = []
    for index, line in data.iterrows():
        print('正在清洗第 {} 条评论... 共 {} 条评论'.format(index + 1, len(data)))
        score = line['scoreList']
        sent = line['reviewList']
        newsent = ''
        wordsCount = 0
        for word in sent.split():
            if word not in stopWords:
                newsent += word + ' '
                wordsCount += 1
        newReview.append(newsent)
        # cleanedData = cleanedData.append({'scores':score, 'reviews':newsent},ignore_index=True)
    cleanedData['reviewList'] = newReview
    print(cleanedData)
    return cleanedData

def dataSaver(data, savepath):
    data.to_csv(savepath, encoding='utf-8-sig',index=0)
    print("清洗数据已保存。数据长度为 {} 。 保存路径 ： {} ".format(len(data), savepath))

if __name__ == '__main__':
    filepath = 'data/p_meta_review_total_3.csv'
    savepath = 'data/c_meta_review_total_3.csv'
    data = dataReader(filepath)
    Dict = createDict(data['reviewList'])
    stopWords = getStopWords(Dict)
    cleanedData = dataCleaner(data, stopWords)
    dataSaver(cleanedData, savepath)