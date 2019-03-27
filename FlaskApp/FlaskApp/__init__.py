#-*- coding: utf-8-*-

# Flask related modules
from flask import Flask, render_template, session, redirect, flash, request


# DB related modules
import pymysql
# Date and Time related modules
import datetime
import time
'''
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
# komoran = Komoran()

@app.route('/')
def homepage():
	return "DB WORKING!"

# Main
if(__name__ == 'main'):
	app.run()

