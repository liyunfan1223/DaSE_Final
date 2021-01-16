# 用于获取metacritic中游戏页面的链接，为进一步爬取评测数据做准备
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

startpage = 0
totpage = 180
nameList = []
linkList = []
for page in range(startpage, totpage + 1):
    print('正在爬取第 {} 页... 共 {} 页'.format(page + 1, totpage))
    url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered'
    if page != 0:
        url = url + '?page=%s' % str(page)
    try:
        req = requests.get(url, timeout = 10, headers = headers)
    except:
        print("服务器访问出错。重试-1")
        try:
            req = requests.get(url, timeout = 10, headers = headers)
        except:
            print("服务器访问出错。重试-2")
            try:
                req = requests.get(url, timeout = 10, headers = headers)
            except:
                print("服务器访问出错。重试-3")
                try:
                    req = requests.get(url, timeout = 10, headers = headers)
                except:
                    print("没救了告辞")

    soup = BeautifulSoup(req.text, 'lxml')

    soups = soup.find_all(href=re.compile(r"/game"),class_="title")

    for i in soups:
        i = i.attrs
        i = i['href']
        name = re.search(r'/game/(\S+)/(\S+)', i).group(2)
        nameList.append(name)
        print('https://www.metacritic.com/' + i + '/critic-reviews')
        linkList.append('https://www.metacritic.com/' + i + '/critic-reviews')

df = pd.DataFrame()
df['name'] = nameList
df['link'] = linkList

df.to_csv('raw_data/mc_links_tot.csv', encoding='utf-8-sig', index = 0)