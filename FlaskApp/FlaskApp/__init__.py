from flask import Flask, render_template, session, redirect, flash, request
import urllib.request
from bs4 import BeautifulSoup
import pymysql

app = Flask(__name__)

# 전체보기 (홈화면)
@app.route('/')
def homepage():
	return render_template('index.html')

# 웹 크롤링 수행
@app.route('/crawl')
def scrapeData():
	scraped_Data = {}

	url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
	request = requests.get(url)
	soup = BeautifulSoup(request.content, "lxml")
	data = soup.find_all('a', {'class': 'cluster_text_headline nclicks(cls_eco.clsart)'})
	for element in data:
		scraped_Data[element.text] = element.get('href')
	return scraped_Data
'''
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
'''
if(__name__ == 'main'):
	app.run()
