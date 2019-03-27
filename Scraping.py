# Crawling related modules
import requests
from gensim.summarization import summarize
from newspaper import Article
from bs4 import BeautifulSoup

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