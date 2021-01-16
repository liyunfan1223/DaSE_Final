# 爬取steam商店页面数据
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def getName(soup):
    try:
        i = soup.find(class_ = "apphub_AppName").text
        name = i
    except:
        name = ""
    return name

def getScores(soup):
    try:
        i = soup.find(class_ = "score high").text
        scores = re.search(r'(\d+)', i).group(1)
    except:
        scores = np.nan
    return scores

def getComments_30days(soup):
    try:
        i = soup.find_all(class_ = "nonresponsive_hidden responsive_reviewdesc")[0].text
        comments = re.search(r'(\S+) 篇用户', i).group(1)
    except:
        comments = np.nan
    return comments

def getRate_30days(soup):
    try:
        i = soup.find_all(class_ = "nonresponsive_hidden responsive_reviewdesc")[0].text
        rate = re.search(r'有 (\d+)% 为好评', i).group(1)
    except:
        rate = np.nan
    return rate

def getComments(soup):
    try:
        i = soup.find_all(class_ = "nonresponsive_hidden responsive_reviewdesc")[1].text
        comments = re.search(r'(\S+) 篇用户', i).group(1)
    except:
        comments = np.nan
    return comments

def getRate(soup):
    try:
        i = soup.find_all(class_ = "nonresponsive_hidden responsive_reviewdesc")[1].text
        rate = re.search(r'有 (\d+)% 为好评', i).group(1)
    except:
        rate = np.nan
    return rate

def getDate(soup):
    try:
        i = soup.find(class_ = "date").text
        date = i
    except:
        date = ""
    return date

def getDeveloper(soup):
    try:
        i = soup.find(class_ = "dev_row").find('a').text
        developer = i
    except:
        developer = ""
    return developer

def getLanguages(soup):
    try:
        i = soup.find(class_ = "all_languages").text
        language = re.search(r'查看所有 (\d*?) 种已支持语言', i).group(1)
    except:
        language = np.nan
    return language

def getPrice(soup):
    try:
        i = soup.find(class_ = "game_purchase_price price").text
        if re.search(r'免费', i) != None:
            price = 0
        else:
            price = re.search(r'¥ (\d*)', i).group(1)
    except:
        try:
            i = soup.find(class_ = "discount_original_price").text
            if re.search(r'免费', i) != None:
                price = 0
            else:
                price = re.search(r'¥ (\d*)', i).group(1)
        except:
            price = np.nan
    return price
def getMetalink(soup):
    # try:
    i = soup.find(href=re.compile(r"https://www.metacritic.com/"))
    if i != None:
        i = i.attrs
        link = i['href']
    else:
        link = ''
    # except:
    #     link = ''
    print(link)
    return link

def getTags(soup):
    try:
        tagList = []
        a = soup.find_all(class_ ="app_tag")
        for i in a:
            i = i.text
            i = i.replace('\r','').replace('\t','').replace('\n','')
            if i == '+':
                pass
            else:
                tagList.append(i)
    except:
        tagList = []
    return tagList

def getContent(url, timeout, headers):
    r = requests.get(url, timeout = timeout)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


if __name__ == '__main__':
    pagestart = 14
    pageend = 500
    for i in range(pagestart, pageend + 1):
        print("正在进行第 %d 轮。" % i)
        path = 'raw_data/steam_link/page%s.csv' % str(i)
        output_path = 'raw_data/games_data%s.csv' % str(i)
        timeout = 10
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        with open(path, 'r') as file:
            df = pd.read_csv(file)



        name = []
        scores = []
        comments_30days = []
        rate_30days = []
        comments = []
        rate = []
        date = []
        developer = []
        languages = []
        price = []
        tags = []
        metalink = []
        error_id = []
        cnt = 0

        for id in df['ID']:
            cnt += 1
            print("正在爬取第 {} 项... 共 {} 项".format(cnt, len(df['ID'])))
            url = 'https://store.steampowered.com/app/%s/?l=schinese' % id
            print(url)
            try: 
                soup = getContent(url, timeout, headers)
            except:
                print("服务器响应出错。再次尝试-1。")
                try:
                    soup = getContent(url, timeout, headers)
                except:
                    try:
                        soup = getContent(url, timeout, headers)
                    except:
                        print("服务器响应出错。再次尝试-2。")
                        try:
                            soup = getContent(url, timeout, headers)
                        except:
                            print("服务器响应出错。再次尝试-3。")
                            try:
                                soup = getContent(url, timeout, headers)
                            except:
                                soup = ''
                                print("服务器响应出错。跳过该项并记录id。")
                                error_id.append(id)
            name.append(getName(soup))
            scores.append(getScores(soup))
            comments_30days.append(getComments_30days(soup))
            rate_30days.append(getRate_30days(soup))
            comments.append(getComments(soup))
            rate.append(getRate(soup))
            date.append(getDate(soup))
            developer.append(getDeveloper(soup))
            languages.append(getLanguages(soup))
            price.append(getPrice(soup))
            tags.append(getTags(soup))
            metalink.append(getMetalink(soup))

        df['name'] = name
        df['scores'] = scores
        df['comments_30days'] = comments_30days
        df['rate_30days'] = rate_30days
        df['comments'] = comments
        df['rate'] = rate
        df['date'] = date
        df['developer'] = developer
        df['languages'] = languages
        df['price'] = price
        df['tags'] = tags
        df['metalink'] = metalink
        print(error_id)

        df.to_csv(output_path, encoding='utf-8_sig', index=0)


            