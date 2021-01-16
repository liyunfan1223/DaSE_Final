# 用于获取steam中游戏商店页面的链接，为进一步爬取评测数据做准备
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

page = 10

def getGameList(page):
    linkList = []
    IDList = []
    nameList = []
    print("正在爬取第 {} 页... 共 {} 页".format(page, totpage))
    try:
        req = requests.get('https://store.steampowered.com/search/?ignore_preferences=1&category1=998&os=win&filter=globaltopsellers&page=%d'%page, timeout = 10)
    except:
        print("again-1")
        try:
            req = requests.get('https://store.steampowered.com/search/?ignore_preferences=1&category1=998&os=win&filter=globaltopsellers&page=%d'%page, timeout = 10)
        except:
            print("again-2")
            try:
                req = requests.get('https://store.steampowered.com/search/?ignore_preferences=1&category1=998&os=win&filter=globaltopsellers&page=%d'%page, timeout = 10)
            except:
                print("again-3")
                try:
                    req = requests.get('https://store.steampowered.com/search/?ignore_preferences=1&category1=998&os=win&filter=globaltopsellers&page=%d'%page, timeout = 10)
                except:
                    print("FAULT!")
    soup = BeautifulSoup(req.text, 'lxml')
    soups = soup.find_all(href=re.compile(r"https://store.steampowered.com/app/"),class_="search_result_row ds_collapse_flag")
    for i in soups:
        i = i.attrs
        i = i['href']
        link = re.match('https://store.steampowered.com/app/(\d*?)/',i).group()
        ID = re.match('https://store.steampowered.com/app/(\d*?)/(.*?)/', i).group(1)
        name = re.match('https://store.steampowered.com/app/(\d*?)/(.*?)/', i).group(2)
        linkList.append(link)
        IDList.append(ID)
    return linkList, IDList

def getdf(page):
    linkList, IDList = getGameList(page)
    df = pd.DataFrame(list(zip(IDList, linkList)),
            columns = ['ID', 'Link'])
    return df

if __name__ == '__main__':
    pagestart = 1
    totpage = pageend = 500
    for i in range(pagestart, pageend + 1):
        path = 'raw_data/steam_link/page%s.csv' % str(i)
        df = getdf(i)
        df.to_csv(path, index=0)