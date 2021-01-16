# 爬取metacritic游戏评分和评测
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

def getContent(url, timeout, headers):
        r = requests.get(url, timeout = timeout, headers = headers)
        soup = BeautifulSoup(r.text, "lxml")
        return soup

if __name__ == '__main__':
    with open('raw_data/meta_link/mc_links_tot.csv','r',encoding='utf-8') as f:
        data = pd.read_csv(f)
    links = data['link']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    timeout = 10
    criticScore = []
    userScore = []
    cnt = 0
    for link in links:
        link = link.replace('/critic-reviews','')
        cnt += 1
        print("{} in {}".format(cnt, len(links)))
        succ = 1
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
    with open('data/meta_reviews_total.csv','r',encoding='utf-8') as f:
        df = pd.read_csv(f)
    # df = df[:3]
    df['criticScore'] = criticScore
    df['userScore'] = userScore
    df.to_csv('data/meta_rivews_total.csv',index=0,encoding='utf-8-sig')