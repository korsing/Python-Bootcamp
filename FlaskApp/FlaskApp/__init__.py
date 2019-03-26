 #-*- coding: utf-8-*-
from flask import Flask, render_template, session, redirect, flash, request
import urllib.request
from bs4 import BeautifulSoup
import pymysql
import requests
from gensim.summarization import summarize
from newspaper import Article
import datetime ########################################################수정

app = Flask(__name__)

# 전체보기 (홈화면)

##JS작업 교체부분############################################################
import datetime
##########################index_main###############################
####table 1#####
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

##########################index2###############################


headlines = ["2019년 불확실성↑, 본원적 경쟁력 강화…SK하이닉스, 정기 주총 개최","이철희 KT 황창규, 수십억 들여 정관계 고문 위촉...로비 의혹!","LG CNS, 전 계열사 IT시스템 90% '구름 위로'",
				"2019년 불확실성↑, 본원적 경쟁력 강화…SK하이닉스, 정기 주총 개최","이철희 KT 황창규, 수십억 들여 정관계 고문 위촉...로비 의혹!","LG CNS, 전 계열사 IT시스템 90% '구름 위로'"];
headlineNum = len(headlines)
headlineUrl = ["https://search.naver.com/p/crd/rd?m=1&px=667&py=1029&sx=667&sy=528&p=U5PqLspVuEhssuvBWJVssssssi8-288258&q=%C7%CF%C0%CC%B4%D0%BD%BA&ssc=tab.nx.all&f=nexearch&w=nexearch&s=PIS3SHZh8lrbCOlvMorRCg==&time=1553443478068&a=nws_all*h.tit&r=2&i=880000AC_000000000000000002071309&g=138.0002071309&u=http%3A//www.ddaily.co.kr/news/article.html%3Fno%3D179183&cr=3",
					"https://www.ytn.co.kr/_ln/0101_201903241103419484",
					"http://www.economytalk.kr/news/articleView.html?idxno=181959",
					"https://search.naver.com/p/crd/rd?m=1&px=667&py=1029&sx=667&sy=528&p=U5PqLspVuEhssuvBWJVssssssi8-288258&q=%C7%CF%C0%CC%B4%D0%BD%BA&ssc=tab.nx.all&f=nexearch&w=nexearch&s=PIS3SHZh8lrbCOlvMorRCg==&time=1553443478068&a=nws_all*h.tit&r=2&i=880000AC_000000000000000002071309&g=138.0002071309&u=http%3A//www.ddaily.co.kr/news/article.html%3Fno%3D179183&cr=3",
					"https://www.ytn.co.kr/_ln/0101_201903241103419484",
					"http://www.economytalk.kr/news/articleView.html?idxno=181959"
					];
contents = ["공정 미세화·수율향상 지속…사회적·재무적 가치 동시 창출 추진 SK하이닉스가 제71기 정기... 22일 SK하이닉스는 경기 이천시 SK하이닉스 영빈관에서 제71기 정기 주총을 열었다. 의결권 있는 주식 77.43%가",
				"[앵커] KT 황창규 회장이 박근혜 정부 시절 정관계 인사들을 이른바 경영 고문으로 위촉해 많게는 수억 원대의 자문료를 주며 각종 민원 해결 등 로비에 활용했다는 주장이 제기됐습니다. 특히 KT 측에 보좌진 특혜",
				"LG CNS, 아시아태평양 클라우드 정보시스템 'TOP 3' 진입",
				"공정 미세화·수율향상 지속…사회적·재무적 가치 동시 창출 추진 SK하이닉스가 제71기 정기... 22일 SK하이닉스는 경기 이천시 SK하이닉스 영빈관에서 제71기 정기 주총을 열었다. 의결권 있는 주식 77.43%가",
				"[앵커] KT 황창규 회장이 박근혜 정부 시절 정관계 인사들을 이른바 경영 고문으로 위촉해 많게는 수억 원대의 자문료를 주며 각종 민원 해결 등 로비에 활용했다는 주장이 제기됐습니다. 특히 KT 측에 보좌진 특혜",
				"LG CNS, 아시아태평양 클라우드 정보시스템 'TOP 3' 진입"];
compName = ["SK하이닉스","KT","LG전자","SK하이닉스","KT","LG전자"];
compPrice = ["76,100(+0.26%)","27,950(+0.0%)","76,100(+2.7%)","76,100(+0.26%)","27,950(+0.0%)","76,100(+2.7%)"];

############################################################################
@app.route('/')
def homepage():
	date = today()
	title=[1,2,3];url=[4,5,6];summary=[7,8,9]
	article_count = len(title)
	return render_template('index_main.html', date = date, companyNames = companyNames, compNum = compNum, keywords = keywords, count = count,
							UserNames = UserNames, OnClick = OnClick, keywords_ranked = keywords_ranked, ranked_count = ranked_count)
	#return render_template('index.html', title=title,url=url,summary=summary,count=article_count)
@app.route('/headlines')
def gather_Headlines():
	year, month, day = today()
	title, url, summary = scrapeData()
	num_of_headlines = len(title)
	return render_template('index_2.html', month = month, day = day)

def scrapeData(url):
	headLine_Title = []
	headLine_Url = []
	headLine_Summary = []

	# 네이버 경제 뉴스 URL
	url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'

	request = requests.get(url)
	soup = BeautifulSoup(request.content, "lxml")
	data = soup.find_all('a', {'class': 'cluster_text_headline nclicks(cls_eco.clsart)'})

	# Scrape된 헤드라인 데이터 중 text 값은 Title로, href 태그는 URL로 저장
	for element in data:
		headLine_Title.append(element.text)
		article_url = element.get('href')
		headLine_Url.append(article_url)
		# newspaper 라이브러리로 기사 본문 발췌
		news = Article(article_url, language='ko')
		news.download()
		news.parse()
		# summarize 함수로 50자로 요약 진행
		headLine_Summary.append(summarize(news.text, word_count=50))

	return headLine_Title, headLine_Url, headLine_Summary


def today():
	calendar = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
	year = datetime.datetime.now().year
	month = calendar[datetime.datetime.now().month-1]
	day = datetime.datetime.now().date().day
	return year, month, day

if(__name__ == 'main'):
	app.run()

'''
def connectDB():
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
