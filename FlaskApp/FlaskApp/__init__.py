from flask import Flask, render_template, session, redirect, flash, request
import urllib.request
from bs4 import BeautifulSoup


app = Flask(__name__)

# 전체보기 (홈화면)
@app.route('/')
def homepage():
	return render_template('index.html')

# 웹 크롤링 수행
@app.route('/crawl'+'<url>)
def scrapeData(url):
	return 'This is Crawling Page'

	'''
	request = urllib.request.Request(url) # url 유효성 검사
	data = urllib.request.urlopen(request, timeout=5).read() # 5초안에 페이지가 안열리면 에러 띄우기
	soup = BeautifulSoup(data, lxml) # 웹사이트 html 코드 전체를 긁어옴
	'''




if(__name__ == 'main'):
	app.run()
