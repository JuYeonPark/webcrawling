# CSS selector 를 이용한 answer

import requests
from bs4 import BeautifulSoup

r=requests.get("http://lambutan.dothome.co.kr/") # 홈페이지 접속
c=r.content # content(내용) 받아옴
soup=BeautifulSoup(c,"html.parser") # beautifulsoup를 사용할수 있게 만들어 줌

aboutexam=soup.select("#ltable > tbody > tr > td.aboutexam.hidden-lg.hidden-md.hidden-sm.hidden-xs")
method=soup.select("#ltable > tbody > tr > td.method.hidden-lg.hidden-md.hidden-sm.hidden-xs")

for item1,item2 in zip(aboutexam,method):
    print(item1.text)
    print(item2.text)
