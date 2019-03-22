import urllib.request
from bs4 import BeautifulSoup
import pymysql
import requests
from gensim.summarization import summarize
from newspaper import Article
from konlpy.tag import Komoran

def scrapeData():
	headLine_Title = []
	headLine_Url = []
	headLine_Summary = []

	# 네이버 경제 뉴스 URL
	url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'

	request = requests.get(url)
	soup = BeautifulSoup(request.content, "lxml")
	data = soup.find_all('a', {'class': 'cluster_text_headline nclicks(cls_eco.clsart)'})
	
	# Scrape된 헤드라인 데이터 중 text 값은 Title로, href 태그는 URL로 저장
	for element in data:
		headLine_Title.append(element.text)
		article_url = element.get('href')
		headLine_Url.append(article_url)
		# newspaper 라이브러리로 기사 본문 발췌
		news = Article(article_url, language='ko')
		news.download()
		news.parse()
		# summarize 함수로 50자로 요약 진행
		headLine_Summary.append(summarize(news.text, word_count=50))
	
	return headLine_Title, headLine_Url, headLine_Summary

a, b, c = scrapeData()

for i in range(len(a)):
    print(a[i])
    print(b[i])
    print(c[i])
