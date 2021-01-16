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
    print(stopWords)
    for key in keys:
        if Dict[key] == 1:
            stopWords.append(key)
    stopWords = set(stopWords)
    print("停用词整理完毕。共 {} 个。".format(len(stopWords)))
    return stopWords

def dataCleaner(data, stopWords):
    cleanedData = pd.DataFrame(columns = ('scores', 'reviews'))
    for index, line in data.iterrows():
        print('正在清洗第 {} 条评论... 共 {} 条评论'.format(index + 1, len(data)))
        score = line[1]
        sent = line[2]
        newsent = ''
        wordsCount = 0
        for word in sent.split():
            if word not in stopWords:
                newsent += word + ' '
                wordsCount += 1
        if wordsCount >= 30:
            cleanedData = cleanedData.append({'scores':score, 'reviews':newsent},ignore_index=True)
    print(cleanedData)
    return cleanedData

def dataSaver(data, savepath):
    data.to_csv(savepath, encoding='utf-8-sig',index=0)
    print("清洗数据已保存。数据长度为 {} 。 保存路径 ： {} ".format(len(data), savepath))

if __name__ == '__main__':
    filepath = 'data/processed_data_reviews.csv'
    savepath = 'data/cleaned_data_reviews_3.csv'
    data = dataReader(filepath)
    Dict = createDict(data['reviews'])
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    wc = WordCloud(
        background_color='white',
        # mask=backgroud_Image,
        # stopwords=STOPWORDS,
        font_path="C:\Windows\Fonts\STZHONGS.TTF",
        max_words=20,
        max_font_size=300,
        # random_state=30,
        width=800,
        height=600
    )
    wc.generate_from_frequencies(Dict)

    wc.to_file('img/wc_words3.png')

    stopWords = getStopWords(Dict)
    
    # cleanedData = dataCleaner(data, stopWords)
    # dataSaver(cleanedData, savepath)