#-*- coding: utf-8-*-

# Modules from Open Source
from flask import Flask, render_template, session, redirect, flash, request

# Modules from Custom Files
from connectDB import *
from scrapeData import *
from dateTime import *

app = Flask(__name__)
'''
x=7;
num = 0;
companyNames = ["(주)LG화학","S-OIL(주)","에스케이네트웍스(주)","에스케이하이닉스(주)","현대모비스(주)","삼성화재해상보험(주)","한국토지주택공사","현대중공업(주)","한국가스공사",
				"(주)포스코","엘지디스플레이(주)","삼성디스플레이(주)","GS칼텍스(주)","삼성생명보험(주)","SK에너지(주)","LG전자(주)","기아자동차(주)","현대자동차(주)","한국전력공사","삼성전자(주)","한국전력공사"];
keywords = [['키워드1_1','키워드1_2','키워드1_3'],['키워드2_1','키워드2_2','키워드2_3'],['키워드3_1','키워드3_2','키워드3_3'],['키워드4_1','키워드4_2','키워드4_3'],['키워드5_1','키워드5_2','키워드5_3'],['키워드6_1','키워드6_2','키워드6_3'],
			['키워드1_1','키워드1_2','키워드1_3'],['키워드2_1','키워드2_2','키워드2_3'],['키워드3_1','키워드3_2','키워드3_3'],['키워드4_1','키워드4_2','키워드4_3'],['키워드5_1','키워드5_2','키워드5_3'],['키워드6_1','키워드6_2','키워드6_3'],
			['키워드1_1','키워드1_2','키워드1_3'],['키워드2_1','키워드2_2','키워드2_3'],['키워드3_1','키워드3_2','키워드3_3'],['키워드4_1','키워드4_2','키워드4_3'],['키워드5_1','키워드5_2','키워드5_3'],['키워드6_1','키워드6_2','키워드6_3'],
			['키워드1_1','키워드1_2','키워드1_3'],['키워드2_1','키워드2_2','키워드2_3'],['키워드3_1','키워드3_2','키워드3_3'],['키워드4_1','키워드4_2','키워드4_3'],['키워드5_1','키워드5_2','키워드5_3'],['키워드6_1','키워드6_2','키워드6_3']];
count = [[1,2,3],[3,4,5],[2,3,4],[3,1,4],[7,3,7],[8,4,7],[1,2,3],[3,4,5],[2,3,4],[3,1,4],[7,3,7],[8,4,7],[1,2,3],[3,4,5],[2,3,4],[3,1,4],[7,3,7],[8,4,7],[1,2,3],[3,4,5],[2,3,4],[3,1,4],[7,3,7],[8,4,7],
		[1,2,3],[3,4,5],[2,3,4],[3,1,4],[7,3,7],[8,4,7]];
compNum = len(companyNames)
####table 2#####
UserNames = ["홍길동","고길동","한수위","Jason","정주용","Peter","최재혁","김날수"];
OnClick = ["한국가스공사","(주)포스코","엘지디스플레이(주)","삼성디스플레이(주)","GS칼텍스(주)","삼성생명보험(주)","SK에너지(주)","LG전자(주)"];
####table 3#####
keywords_ranked = ["키워드랭크1","키워드랭크2","키워드랭크3","키워드랭크4","키워드랭크5","키워드랭크6","키워드랭크7","키워드랭크8","키워드랭크9","키워드랭크10"];
ranked_count = [15,12,11,10,8,7,5,4,3,2]
'''

@app.route('/')
def homepage():
	return "GEKKO WORLD!"
	'''
	date = today()
	title=[1,2,3];url=[4,5,6];summary=[7,8,9]
	article_count = len(title)
	return render_template('index_main.html', date = date, companyNames = companyNames, compNum = compNum, keywords = keywords, count = count,
							UserNames = UserNames, OnClick = OnClick, keywords_ranked = keywords_ranked, ranked_count = ranked_count)
	#return render_template('index.html', title=title,url=url,summary=summary,count=article_count)
	'''
@app.route('/headlines')
def gather_Headlines():
	date = today()
	title, url = scrapeData()
	num_of_headlines = len(title)
	return render_template('index_2.html', date = date, titles = title, urls = url, num_of_headlines = num_of_headlines)


if(__name__ == 'main'):
	app.run()


