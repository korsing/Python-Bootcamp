from flask import Flask, render_template, session, redirect, flash, request
import urllib.request
from bs4 import BeautifulSoup
import pymysql

app = Flask(__name__)

# 전체보기 (홈화면)
@app.route('/')
def homepage():
	return render_template('index.html')


def Scrape_DB(scraped_Data):
	db = pymysql.connect(host="localhost", user="root", passwd="skgkdlslrtm", db="Bootcamp", charset='utf8')
	cur = db.cursor()
	# 현재 
	cur.execute("SELECT max(seq) from scrape;")
	maxseq = cur.fetchone()[0]
	if(maxseq != None):
		cur.execute("INSERT INTO scrape (seq, title, url) VALUES ({},{},{})".format(maxseq+1, titles))
	db.commit()
	db.close()

# 웹 크롤링 수행
def scrapeData():
	headLine_Title = []
	headLine_Url = []

	url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
	request = requests.get(url)
	soup = BeautifulSoup(request.content, "lxml")
	data = soup.find_all('a', {'class': 'cluster_text_headline nclicks(cls_eco.clsart)'})
	for element in data:
		headLine_Title.append(element.text)
		headLine_Url.append(element.get('href'))
	for i in range(len(headLine_Title)):
		print(headLine_Title[i], ": ", headLine_Url[i])


if(__name__ == 'main'):
	app.run()
