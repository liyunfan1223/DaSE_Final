# 用于爬取metacritic游戏评分，并和steam数据合并
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

def getContent(url, timeout, headers):
        r = requests.get(url, timeout = timeout, headers = headers)
        soup = BeautifulSoup(r.text, "lxml")
        return soup

def crawl(ii):
    print('第{}页：'.format(ii))
    with open('raw_data/games_data/games_data%s.csv'%str(ii),'r',encoding='utf-8')as f:
        data = pd.read_csv(f)
    data = data.loc[data['metalink'] == data['metalink']]

    links = data['metalink']

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    timeout = 10
    

    criticScore = []
    userScore = []
    scoreList = []
    reviewList = []
    for link in links:
        print(link)
        succ = 1
        
        if link != '':
            try: 
                soup = getContent(link, timeout, headers)
            except:
                print("服务器响应出错。再次尝试-1。")
                try:
                    soup = getContent(link, timeout, headers)
                except:
                    try:
                        soup = getContent(link, timeout, headers)
                    except:
                        print("服务器响应出错。再次尝试-2。")
                        try:
                            soup = getContent(link, timeout, headers)
                        except:
                            print("服务器响应出错。再次尝试-3。")
                            try:
                                soup = getContent(link, timeout, headers)
                            except:
                                soup = ''
                                print("没救了告辞")
                                succ = 0
            if succ:
                i = soup.find(class_ = 'metascore_w xlarge game positive')
                if i == None:
                    i = soup.find(class_ = 'metascore_w xlarge game mixed')
                    if i == None:
                        i = soup.find(class_ = 'metascore_w xlarge game negative')
                if i != None:
                    criticScore.append(i.text)
                else: 
                    criticScore.append(np.nan)

                i = soup.find(class_ = 'metascore_w user large game positive')
                if i == None:
                    i = soup.find(class_ = 'metascore_w user large game mixed')
                    if i == None:
                        i = soup.find(class_ = 'metascore_w user large game negative')
                if i != None:
                    userScore.append(i.text)
                else: 
                    userScore.append(np.nan)

                
                criLink = link + '/critic-reviews'
                print(criLink)
                try: 
                    soup = getContent(criLink, timeout, headers)
                except:
                    print("服务器响应出错。再次尝试-1。")
                    try:
                        soup = getContent(criLink, timeout, headers)
                    except:
                        try:
                            soup = getContent(criLink, timeout, headers)
                        except:
                            print("服务器响应出错。再次尝试-2。")
                            try:
                                soup = getContent(criLink, timeout, headers)
                            except:
                                print("服务器响应出错。再次尝试-3。")
                                try:
                                    soup = getContent(criLink, timeout, headers)
                                except:
                                    soup = ''
                                    print("没救了告辞")
                                    succ = 0
                soups = soup.find_all(attrs={"class" :"metascore_w medium game positive indiv perfect"})
                scores = []
                reviews = []
                for i in soups:
                    scores.append(i.text)
                soups = soup.find_all(attrs={"class" :"metascore_w medium game positive indiv"})
                for i in soups:
                    scores.append(i.text)
                soups = soup.find_all(attrs={"class" :"metascore_w medium game mixed indiv"})
                for i in soups:
                    scores.append(i.text)
                soups = soup.find_all(attrs={"class" :"metascore_w medium game negative indiv"})
                for i in soups:
                    scores.append(i.text)

                soups = soup.find_all(attrs={"class" :"review_body"})
                for i in soups:
                    review = i.text.replace('\t','').replace('\n','').replace('  ','')
                    reviews.append(review)
                t1 = []
                t2 = []
                for i in range(len(scores)):
                    t1.append(scores[i])
                    t2.append(reviews[i])
                scoreList.append(t1)
                reviewList.append(t2)
            else:
                criticScore.append(np.nan)
                userScore.append(np.nan)
                scoreList.append([])
                reviewList.append([])

    data['criticScores'] = criticScore
    data['userScores'] = userScore
    data['scoreList'] = scoreList
    data['reviewList'] = reviewList

    data.to_csv('raw_data/steam_info/crawled_info%s.csv'%str(ii), index = 0, encoding='utf-8-sig')

if __name__ == '__main__':
    for i in range(1, 501):
        crawl(i)