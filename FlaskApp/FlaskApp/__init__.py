#-*- coding: utf-8-*-

# Flask related modules
from flask import Flask, render_template, session, redirect, flash, request
# DB related modules
import pymysql
# Date and Time related modules
import datetime
import time
# Crawling related modules
import requests
from gensim.summarization import summarize
from newspaper import Article
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def homepage():

	return render_template('index.html', date = date, companyNames = companyNames, compNum = compNum, keywords = keywords, count = count,
							UserNames = UserNames, OnClick = OnClick, keywords_ranked = keywords_ranked, ranked_count = ranked_count)
	#return render_template('index.html', title=title,url=url,summary=summary,count=article_count)

@app.route('/headlines')
def gather_Headlines():
	date = today()
	title, url = scrapeData()
	num_of_headlines = len(title)
	return render_template('headlines.html', date = date, titles = title, urls = url, num_of_headlines = num_of_headlines)


# Custom Functions
def connectDB():
	conn = pymysql.connect(host="localhost", user="root", passwd="skgkdlslrtm", db="Bootcamp", charset='utf8')
	c = conn.cursor()
	return c, conn

def today():
	calendar = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
	year = datetime.datetime.now().year
	month = calendar[datetime.datetime.now().month-1]
	day = datetime.datetime.now().date().day
	return year, month, day

def scrapeData():
	# NAVER SCRAPYING
	
	headline_Naver = []
	url_Naver = []

	# 네이버 경제 뉴스 URL
	url_Economy = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
	url_Stock = 'https://finance.naver.com/news/news_list.nhn?mode=LSS3D&section_id=101&section_id2=258&section_id3=402'

	req_Economy = requests.get(url_Economy)
	req_Stock = requests.get(url_Stock)

	soup_Economy = BeautifulSoup(req_Economy.content, "lxml")
	soup_Stock = BeautifulSoup(req_Stock.content, "lxml")

	headlines_Economy = soup_Economy.find_all('a', {'class': 'cluster_text_headline nclicks(cls_eco.clsart)'})
	headlines_Stock = soup_Stock.find_all('dd',{'class':'articleSubject'})

	for title in headlines_Economy:
		headline_Naver.append(title.text)
		url_Naver.append(title.get('href'))
	for title in headlines_Stock:
		headline_Naver.append(title.text)
		url_Naver.append('https://finance.naver.com' + title.find('a').get('href'))
	
	# URL 던져주면 요약해주는 함수 실행
	
	return headline_Naver, url_Naver
# Main
if(__name__ == 'main'):
	app.run()


