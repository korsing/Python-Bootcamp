 #-*- coding: utf-8-*-
from flask import Flask, render_template, session, redirect, flash, request
import urllib.request
from bs4 import BeautifulSoup
import pymysql
import requests
from gensim.summarization import summarize
from newspaper import Article

app = Flask(__name__)

# 전체보기 (홈화면)
@app.route('/')
def homepage():
	scrapeData()
	return render_template('index.html')

def scrapeData(url):
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

if(__name__ == 'main'):
	app.run()

'''
def connectDB():
	db = pymysql.connect(host="localhost", user="root", passwd="skgkdlslrtm", db="Bootcamp", charset='utf8')
	cur = db.cursor()
	# 현재 
	cur.execute("SELECT max(seq) from scrape;")
	maxseq = cur.fetchone()[0]
	if(maxseq != None):
		cur.execute("INSERT INTO scrape (seq, title, url) VALUES ({},{},{})".format(maxseq+1, titles))
	db.commit()
	db.close()
'''
