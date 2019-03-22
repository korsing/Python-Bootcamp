import urllib.request
from bs4 import BeautifulSoup
import pymysql
import requests
from gensim.summarization import summarize
from newspaper import Article
from konlpy.tag import Komoran

komoran = Komoran()
def scrapeData():
    headLine_Title = []
    headLine_Url = []
    headLine_Summary = []

    url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
    request = requests.get(url)
    soup = BeautifulSoup(request.content, "lxml")
    data = soup.find_all('a', {'class': 'cluster_text_headline nclicks(cls_eco.clsart)'})
    for element in data:
        headLine_Title.append(element.text)
        headLine_Url.append(element.get('href'))
    '''
    for article_url in headLine_Url:
        news = Article(article_url, language='ko')
        news.download()
        news.parse()
        headLine_Summary.append(summarize(news.text, word_count=50))
    '''
    return headLine_Title

temp = scrapeData()

for title in temp:
    print(komoran.nouns(title))
    print("\n\n\n\n\n")

