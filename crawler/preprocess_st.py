# 数据预处理
import pandas as pd
import numpy as np

def dataReader(filepath):
    with open(filepath,'r',encoding='utf-8') as f:
        data = pd.read_csv(f)
    print("数据加载完成。数据长度为 {} 。".format(len(data)))
    return data

if __name__ == '__main__':
    filepath = 'data/meta_reviews_total.csv'
    data = dataReader(filepath)
    filepath2 = 'data/meta_reviews_total_2.csv'
    data2 = dataReader(filepath2)
    filepath3 = 'raw_data/meta_link/mc_links_tot.csv'
    data3 = dataReader(filepath3)
    lll = []
    for link in data3['link']:
        link = link.replace('.com//','.com/').replace('/critic-reviews','')
        lll.append(link + '?ftag=MCD-06-10aaa1f')
    print(len(data), len(lll))
    data['link'] = lll
    
    data['userScore'] = data2['userScore']
    data['criticScore'] = data2['criticScore']
    data = data.dropna()
    data = data.loc[data['scoreList'] != '[]']
    data = data.loc[data['reviewList'] != '[]']
    reviewList = data['reviewList']
    newreviewList = []
    for reviews in reviewList:        
        reviews = reviews.replace('\'','').replace('[','').replace(']','').replace(',','').replace('.','').replace('"','').replace('\\','')
        reviews = reviews.lower()
        newreviewList.append(reviews)
    scoreList = data['scoreList']
    newscoreList = []
    for score in scoreList:
        score = score.replace('[','').replace('\'','').replace(']','')
        score = score.split(',')
        SUM = 0
        for i in score:
            SUM += int(i)
        newscoreList.append(SUM / len(score))
    print(newscoreList)
    
    data['scoreList'] = newscoreList
    data['reviewList'] = newreviewList
    
    data.to_csv('data/p_meta_review_total_3.csv',index=0, encoding='utf-8-sig')