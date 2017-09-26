import requests
from bs4 import BeautifulSoup

r=requests.get("http://lambutan.dothome.co.kr/") # 홈페이지 접속
c=r.content # content(내용) 받아옴
soup=BeautifulSoup(c,"html.parser") # beautifulsoup를 사용할수 있게 만들어 줌


all=soup.find("tbody") # tbody 라는 태그를 찾아 all이라는 변수에 저장
all2=all.find_all("tr",{"class":""}) # 각 행(tr태그이면서 class는 공백인)을 all2에 저장

for item in all2: # 각 행을 for 문으로 돌면서
    professor=item.find("td",{"class":"professor"}).text # td 라는 태그 class 는 professor(교수)를 찾는다
    lectureName=item.find("td",{"class":"lecture"}).text # td 라는 태그 class 는 lecture(강의)를 찾는다
    orther=item.find("td",{"class":"orther"}).text # 이하 같음
    grade = item.find("td", {"class": "grade"}).text
    evaluation=item.find("td", {"class": "evaluation"}).text
    print(professor + " / " + lectureName + " / " + orther + " / " + grade + " / " + evaluation) #  출력