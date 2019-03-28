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
import urllib.parse
import urllib.request

# Threading related modules
import threading

# Keyword Extraction related modules
from sklearn.feature_extraction.text import TfidfVectorizer
#from konlpy.tag import Komoran
from collections import Counter
import numpy as np


# 전역변수 선언
app = Flask(__name__)
#komoran = Komoran()

@app.route('/')
def homepage():
    c, conn = connectDB()
    #c.execute("SELECT COUNT(seq) from seq_company;")
    count  =10
    
    c.execute("SELECT title from article;")
    headline = c.fetchall()

    c.execute("SELECT company from seq_company;")
    seq_company = c.fetchall()
    
    c.execute("SELECT keyword from seq_key;")
    seq_key = c.fetchall()
    
    conn.close()
    return render_template('dashboard.html', count=count, headline=headline, seq_company=seq_company, seq_key=seq_key)




@app.route('/headlines')
def gather_Headlines():
	date = today()
	c, conn = connectDB()
	c.execute("SELECT title from article;")
	title = c.fetchall()
	c.execute("SELECT article_url from article;")
	url = c.fetchall()

	num_of_headlines = len(title)
	conn.close()
	return render_template("headlines.html", titles = title, urls = url, date = date, num_of_headlines = num_of_headlines)

@app.route('/refresh')
def refresh():
   scrapeArticles()
   return redirect('/')
   
def today():
	calendar = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
	year = datetime.datetime.now().year
	month = calendar[datetime.datetime.now().month-1]
	day = datetime.datetime.now().date().day
	return year, month, day

def connectDB():
	conn = pymysql.connect(host="localhost", user="root", passwd="skgkdlslrtm", db="Bootcamp", charset='utf8mb4')
	c = conn.cursor()
	return c, conn


def UrltoKeyword(urls, weight):
    print("UrltoKeyword Function Started!")
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

def CnameandKeyword(keyword, keyword_weight,company_list_1): # text에서 keyword, 회사명 뽑기
    print("CnameandKeyword Function Started!")
    c, conn = connectDB()
    # 회사이름, url번호
    c_name_from_list_1 = []
    for i in range(len(keyword)):
        for j in range(len(company_list_1)):               
            if keyword[i][0] ==( company_list_1[j].lower() or company_list_1[j].upper()): 
                c_name_from_list_1.append([company_list_1[j],keyword[i][1]])
                c.execute("INSERT INTO seq_company (company,seq) VALUES %s, %d;",(company_list_1[j], keyword[i][1]))
                c.commit()


                        

    temp = []
    for com_name in c_name_from_list_1:
        temp.append(com_name[0])
        
    # keyword, url번호
    keyword_from_list = []    
    for i in range(len(keyword)):
        if(keyword[i][0] not in temp):
            keyword_from_list.append(keyword[i])
            c.execute("INSERT INTO seq_key (keyword,seq) VALUES %s, %d;",(keyword[i][0], keyword[i][1]))
            c.commit()

    
    c.commit()
    conn.close()           

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

    
# 각종 뉴스 포털에서 기사 제목, 링크 갖다 DB에 추가
def scrapeArticles():
    print("scrapeArticles Function Started!")
    # NAVER SCRAPYING
    year = datetime.datetime.now().date().year
    month = datetime.datetime.now().date().month
    day = datetime.datetime.now().date().day

    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)

    headline = []
    url = []

    # 네이버 /네이트 경제 뉴스 URL
    url_Economy = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
    url_Stock = 'https://finance.naver.com/news/news_list.nhn?mode=LSS3D&section_id=101&section_id2=258&section_id3=402'
    url_Economy_Nate = 'https://news.nate.com/subsection?cate=eco01&mid=n0305&type=t&date=%d%s%s' % (year, month, day)

    req_Economy = requests.get(url_Economy)
    req_Stock = requests.get(url_Stock)
    req_Economy_Nate = requests.get(url_Economy_Nate)

    soup_Economy = BeautifulSoup(req_Economy.content, "lxml")
    soup_Stock = BeautifulSoup(req_Stock.content, "lxml")
    soup_Economy_Nate = BeautifulSoup(req_Economy_Nate.content, "lxml")

    headlines_Economy = soup_Economy.find_all('a', {'class': 'cluster_text_headline nclicks(cls_eco.clsart)'})
    headlines_Stock = soup_Stock.find_all('dd', {'class': 'articleSubject'})
    headlines_Economy_Nate = soup_Economy_Nate.find_all('ul', {"class": "mduSubject"})

    for title in headlines_Economy:
        headline.append(title.text)
        url.append(title.get('href'))
    for title in headlines_Stock:
        headline.append(title.text)
        url.append('https://finance.naver.com' + title.find('a').get('href'))

    for i in range(len(headlines_Economy_Nate)):
        for j in range(len(headlines_Economy_Nate[i].findAll('a'))):
            headline.append(headlines_Economy_Nate[i].findAll('a')[j].text)
            url.append('https://news.nate.com/' + headlines_Economy_Nate[i].findAll('a')[j].get('href'))
    '''
    logo = ''
    for i in url:
        if 'naver' in i:
            logo = 'naver'
        else:
            logo = 'nate'

    new_index = [i for i in range(len(headline))]
    new_index = shuffle(new_index)
    '''
    # DB에 추가하는 함수 실행

    c, conn = connectDB()
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    query = "INSERT INTO article (title, article_url, date, contents) VALUES (%s, %s, %s, %s)"
    for count in range(len(headline)):
        c.execute(query, (headline[count], url[count], now, 'summary goes here')) #<--요약봇 ㅜㅡㅜㅜㅡㅜ
    conn.commit()
    
    c.execute("SELECT article_url from article;")
    temp  = c.fetchall()
    url_list = [i[0] for i in temp]
    #print(url_list)
    c.execute("SELECT name from company;")
    temp =  c.fetchall()
    com_list =  [i[0] for i in temp]

    A, B = UrltoKeyword(url_list, 0.1)

    _A, _B, _C  = CnameandKeyword(A,B,com_list)

    relatedTokeyword(_A,_B,_C)

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

'''
 #backend func -
def Select_Seq(url):
    c, conn = connectDB()
    c.execute("SELECT seq from article where article_url = %s;",url)
    seq= c.fetchall()
    conn.close()
    return seq
'''

#Seq_com, Seq_Key 테이블에 회사명/키워드 삽입  #이미 있는 headline이면 insert 막는다
'''
def insert_Seq_Comp_Key(companylist, keywordlist,seq):
    
    newCompanylst =','.join(i for i in companylist)
    newKeywordlist = ','.join(i for i in keywordlist)
    c, conn = connectDB()
    query_com = "INSERT INTO seq_company VALUES (%d, %s);"
    query_key = "INSERT INTO seq_key VALUES (%d, %s);"
    c.execute(query_com,(seq, newCompanylst))
    c.execute(query_key, (seq, newKeywordlist))
    c.commit()
    conn.close()
'''
'''

#Matchs 테이블 채우기
def insert_Matchs():

    c,conn = connectDB()
    query_com = "SELECT company FROM seq_company;"
    c.execute(query_com)
    com_Tuple = c.fetchall()
    li_com_Tuple = str(com_Tuple[0]).split(',')

    for i in li_com_Tuple:
        c.execute("SELECT code from company where name=%s;",i)
        i_code = c.fetchone()
        i_code = str(i_code[0])
        c.execute("INSERT INTO Matchs (name, code) VALUES (%s,%s);",(i,i_code))
        query_keyword = ("SELECT keyword from seq_keyword k, seq_company c where k.seq=c.seq and where c.companies=%s;",i)
        c.execute(query_keyword)
        keyword_Tuple= c.fetchone()[0]
        str_keyword= ','.join(keyword_Tuple)
        c.execute("INSERT INTO Matchs (keyword) VALUES (%s);",str_keyword)

    c.commit()
    conn.close()


#userid 입력받아서 기사별 선호도 추출, weight순으로 prefered keyword 생성

def User(userid):

    dict_for_prefer ={}
    c, conn = connectDB()
    c.execute("SELECT seq FROM User where userid = %s;",userid)
    user_seq = c.fetchone
    userstring= str(user_seq[0])
    usersplit = userstring.split(',')

    for i in usersplit:
        if usersplit.index(i) == 0:
            c.execute("SELECT keyword FROM seq_key where seq = %s;",i)
            temp = c.fetchone()
            temp = str(temp[0]).split(',')
            for j in temp :
                dict_for_prefer[j] = 1

        else:
            c.execute("SELECT keyword FROM seq_keyword where seq = %s;", i)
            temp = c.fetchone()
            temp = str(temp[0]).split(',')
            for j in temp :
                if j in dict_for_prefer.keys():
                    dict_for_prefer[j] +=1
                else:
                    dict_for_prefer[j] = 1
    dict_for_prefer = sorted(dict_for_prefer, key=dict_for_prefer.get )[::-1]
    c.execute("INSERT INTO users (pref_key1, pref_key2, pref_key3) VALUES (%s %s %s);",(dict_for_prefer[0],dict_for_prefer[1],dict_for_prefer[2]))
    c.commit()
    conn.close()

   
#---
 '''  
# Main
if(__name__ == 'main'):
	app.run()

