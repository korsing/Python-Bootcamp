from newspaper import Article
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Komoran
from collections import Counter
import numpy as np
import os
import urllib.parse
import urllib.request
import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize 
import time 
import pymysql

komoran = Komoran()
urls = []

def connectDB():
    conn = pymysql.connect(host="localhost", user="root", passwd="skgkdlslrtm", db="Bootcamp", charset='utf8mb4')
    c = conn.cursor()
    return c, conn
    
c, conn = connectDB()
c.execute("SELECT name from company;")
temp = c.fetchall()
company_list_1 = [temp[i][0] for i in range(len(temp))]



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
        for j in range(len(company_list_1)):               
            if keyword[i][0] ==( company_list_1[j].lower() or company_list_1[j].upper()): 
                c_name_from_list_1.append([company_list_1[j],keyword[i][1]])
                         
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
timee=5#time
for t in range(1):
    time.sleep(timee)
    print(t,'wow')
    
    url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
    
    request = requests.get(url)
    soup = BeautifulSoup(request.content, "lxml")
    data = soup.find_all('a', {'class': 'cluster_text_headline nclicks(cls_eco.clsart)'})
    
    for element in data:
        article_url = element.get('href')
        urls.append(article_url)  
      
        
    keyword, keyword_weight = UrltoKeyword(urls, 0.2)
    keyword_from_list, c_name_from_list_1, temp=CnameandKeyword(keyword, keyword_weight,company_list_1,company_list_2,company_list)
    keyword_from_c_name=relatedTokeyword(keyword_from_list, c_name_from_list_1, temp) 
    
    #%%
    counter_c_name=Counter(temp)
    noti_c_name = counter_c_name.most_common(1)
    print(noti_c_name)
    
     
        
