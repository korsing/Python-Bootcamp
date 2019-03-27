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
	return render_template("dashboard.html")

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

# Main
if(__name__ == 'main'):
	app.run()

