#-*- coding: utf-8-*-

# Flask related modules
from flask import Flask, render_template, session, redirect, flash, request
'''
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
import urllib.parse
import urllib.request
# Threading related modules
import threading

# Keyword Extraction related modules
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Komoran
from collections import Counter
import numpy as np
'''

# 전역변수 선언
app = Flask(__name__)
#komoran = Komoran()

@app.route('/')
def homepage():
	return "DB WORKING!"
	#return render_template('index.html', date = date, companyNames = companyNames, compNum = compNum, keywords = keywords, count = count,
	#						UserNames = UserNames, OnClick = OnClick, keywords_ranked = keywords_ranked, ranked_count = ranked_count)
	#return render_template('index.html', title=title,url=url,summary=summary,count=article_count)
'''
@app.route('/headlines')
def gather_Headlines():
	date = today()
	c, conn = connectDB()
	c.execute("SELECT title from article;")
	title = c.fetchall()
	c.execute("SELECT article_url from article;")
	url = c.fetchall()

	num_of_headlines = len(title)
	
	return render_template('headlines.html', date = date, titles = title, urls = url, num_of_headlines = num_of_headlines)

@app.route('/dashboard')
def crawl():
	c, conn = connectDB()
	c.execute("SELECT seq, title, article_url, date FROM article;")
	data = c.fetchall()
	len_data = len(data)
	conn.close()
	return render_template('dashboard.html', data = data, len_data = len_data)

@app.route('/refresh')
def refresh():
	scrapeArticles()
	return redirect('/dashboard')

# Custom Functions
def connectDB():
	conn = pymysql.connect(host="localhost", user="root", passwd="skgkdlslrtm", db="Bootcamp", charset='utf8mb4')
	c = conn.cursor()
	return c, conn

def today():
	calendar = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
	year = datetime.datetime.now().year
	month = calendar[datetime.datetime.now().month-1]
	day = datetime.datetime.now().date().day
	return year, month, day

# 각종 뉴스 포털에서 기사 제목, 링크 갖다 DB에 추가
def scrapeArticles():
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

	insertDB('article', [headline_Naver, url_Naver])

def insertDB(table, value):
	return table # 디버깅용 프린트
	c, conn = connectDB()
	if(table == 'article'):
		title = value[0]
		url = value[1]
		now = datetime.datetime.now().strftime('%Y-%m-%d')
		query = "INSERT INTO article (title, article_url, date, sum, key_1, key_2, key_3) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		for count in range(len(headline_Naver)):
			flag = c.execute("SELECT title FROM article where title = %s;", (headline_Naver[count]))
			if(flag == 0):
				c.execute(query,(title[count], url[count], now, '0','0','0','0'))
	elif(table == 'seq_com'):
		return "seq_com의 경우"
	elif(table == 'seq_key'):
		return "seq_key의 경우"
	elif(table == 'matchs'):
		return "matchs의 경우"
	elif(table == 'users'):
		return "users의 경우"
	else:
		return "NOT VALID TABLE NAME"
	conn.commit()
	conn.close()

def get_StockPrice(code):
	req_Stock = requests.get('https://finance.naver.com/item/main.nhn?code='+code)
	soup_Stock = BeautifulSoup(req_Stock.content, 'lxml')

	price_tag = soup_Stock.find_all('p', {'class': 'no_today'})
	variation_tag = soup_Stock.find_all('em', {'class': 'no_down'})

	price = price_tag[0].contents[1].contents[1].text
	if(variation_tag[2].contents[1].text=='-'):
		variation = eval(variation_tag[2].contents[3].text)*-1
	elif(variation_tag[2].contents[1].text=='+'):
		variation = eval(variation_tag[2].contents[3].text)
	else:
		return None
	return price, variation

def urlstoKeywords(urls,weight): # text에서 keyword, 회사명 뽑기
    article_text_noun = []
    ## article_text_noun 뽑
    for temp in range(len(urls)):
        article= Article(urls[temp],language='ko')
        article.download()
        article.parse()
        article_text_= article.text    
        article_text_ = "".join([s for s in article_text_.strip().splitlines(True) if s.strip()])
        temp_ = ' '.join(komoran.nouns(article_text_))
        article_text_noun.append(temp_)
        
    ## tfidf_알고리즘 , keyword , keyword weight 뽑
    tfidf_vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(article_text_noun)
    keyword_weight_ = tfidf_matrix.toarray()
    keyword_ = tfidf_vectorizer.get_feature_names()
    
    # keyword 와 회사이름 뽑
    n=0
    keyword=[]
    keyword_weight=[]
    for i in range(len(keyword_weight_)):
        for j in range(len(keyword_weight_[0])):
            if keyword_weight_[i,j] > weight : 
                keyword.append(keyword_[j])
                keyword_weight.append(keyword_weight_[i,j])     
                
    company_list = read_csv_file('companylist.csv',index=True)
    company_list_1 = [company_list[i][0] for i in range(len(company_list))]
    company_list_2 = [komoran.nouns(company_list[i][1]) for i in range(len(company_list))]
    
    # 회사이름, url번호
    c_name_from_list_1 = []
    for i in range(len(keyword)):                  
        if keyword[i][0] in company_list_1 : c_name_from_list_1.append([keyword[i][0],keyword[i][1]])
                     
    temp = []
    for com_name in c_name_from_list_1:
        temp.append(com_name[0])
        
    # keyword, url번호
    keyword_from_list = []    
    for i in range(len(keyword)):
        if(keyword[i][0] not in temp):
            keyword_from_list.append(keyword[i])
    
    return keyword_from_list, c_name_from_list_1, temp


#%%
company_list = read_csv_file('companylist.csv',index=True)
company_list_1 = [company_list[i][0] for i in range(len(company_list))]
company_list_2 = [komoran.nouns(company_list[i][1]) for i in range(len(company_list))]

 # 기사 URL
def UrltoKeyword(urls, weight):
    
    article_text_noun = []
    ## article_text_noun 뽑
    for temp in range(len(urls)):
        article= Article(urls[temp],language='ko')
        article.download()
        article.parse()
        article_text_= article.text    
        article_text_ = "".join([s for s in article_text_.strip().splitlines(True) if s.strip()])
        temp_ = ' '.join(komoran.nouns(article_text_))
        article_text_noun.append(temp_)
        
    ## tfidf_알고리즘 , keyword , keyword weight 뽑
    tfidf_vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(article_text_noun)
    keyword_weight_ = tfidf_matrix.toarray()
    keyword_ = tfidf_vectorizer.get_feature_names()
    
    

    a=[]
    keyword=[]
    keyword_weight=[]
    wei=weight
    for i in range(len(keyword_weight_)):
        for j in range(len(keyword_weight_[0])):
            if keyword_weight_[i,j] > wei: 
                keyword.append([keyword_[j],i])
                keyword_weight.append([keyword_weight_[i,j],i])
                a.append(article_text_noun[i])     
                
    return keyword, keyword_weight

    
def CnameandKeyword(keyword, keyword_weight,company_list_1,company_list_2,company_list): # text에서 keyword, 회사명 뽑기

       
    # 회사이름, url번호
    c_name_from_list_1 = []
    for i in range(len(keyword)):                  
        if keyword[i][0] in company_list_1 : c_name_from_list_1.append([keyword[i][0],keyword[i][1]])
                     
    temp = []
    for com_name in c_name_from_list_1:
        temp.append(com_name[0])
        
    # keyword, url번호
    keyword_from_list = []    
    for i in range(len(keyword)):
        if(keyword[i][0] not in temp):
            keyword_from_list.append(keyword[i])
    
    return keyword_from_list, c_name_from_list_1, temp
    

    
def relatedTokeyword(keyword_from_list, c_name_from_list_1, temp):
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
    temp = list(set(temp)) 
    
    related_word = []
    for i in range(len(temp)):
        search = temp[i]
    
        query = url + search
        r = requests.get(query)
    
        soup = BeautifulSoup(r.content, 'lxml')
        soup2 = soup.find_all('ul',{'class':'_related_keyword_ul'})
        
        related_word_ = []
        for j in soup2:
            related_word_.append(j.text.split("  "))
        related_word.extend(related_word_)
    
    # 연관검색어 keyword 추가
    rr = []
    for i in related_word:
        rr2 = []     
        for j in i:
            if(len(j)):
                for k in j.split():
                    if(k not in rr):
                        rr2.append(k)
        rr.append(rr2)
    
    rr = [list(set(rr[i])) for i in range(len(rr))]    
    keyword_from_c_name = {temp[i]:rr[i][1:7] for i in range(len(rr))}   
    
    k=[]
    for i in range(len(c_name_from_list_1)):
        for j in range(len(keyword_from_list)):
            if c_name_from_list_1[i][1] == keyword_from_list[j][1]:
                if( [c_name_from_list_1[i][0],keyword_from_list[j][0]] not in k):
                    k.append([c_name_from_list_1[i][0],keyword_from_list[j][0]])
                
    #뉴스 본문 keyword 추가    
    for i in temp :
        for j in range(len(k)):
            if k[j][0] == i:
                keyword_from_c_name[i].append(k[j][1])
            
    return keyword_from_c_name        
 #%% 
'''
# Main
if(__name__ == 'main'):
	app.run()

