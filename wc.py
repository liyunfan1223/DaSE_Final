# 词云
import pickle
from os import path
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd


backgroud_Image = plt.imread('img/steam_logo.jpg')


wc = WordCloud(
    background_color='white',
    # mask=backgroud_Image,
    stopwords=STOPWORDS,
    font_path="C:\Windows\Fonts\STZHONGS.TTF",
    max_words=20,
    max_font_size=150,
    # random_state=30,
    width=800,
    height=600
)

with open('datasets/meta_reviews_total.csv', encoding='utf-8') as file:
    data = pd.read_csv(file)

text = ''
cnt = 0
for review in data['reviewList']:
    cnt += 1
    print("{} in {}".format(cnt, len(data)))
    text += review + ' '
'''
for tags in data['tags']:
    for word in tags.split(','):
        word = word.replace("'",'').replace('[','').replace(']','').replace(' ','')
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
'''
# frequency = sorted(frequency.items(), key=lambda item:item[1], reverse=True)

wc.generate_from_text(text)

wc.to_file('img/wc_words.png')

