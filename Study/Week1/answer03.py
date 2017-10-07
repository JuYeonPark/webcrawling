import requests
from bs4 import BeautifulSoup

r=requests.get("http://lambutan.dothome.co.kr/") # 홈페이지 접속
c=r.content # content(내용) 받아옴
soup=BeautifulSoup(c,"html.parser") # beautifulsoup를 사용할수 있게 만들어 줌


all=soup.find("tbody") # tbody 라는 태그를 찾아 all이라는 변수에 저장
all2=all.find_all("tr",{"class":""}) # 각 행(tr태그이면서 class는 공백인)을 all2에 저장

for item in all2: # 각 행을 for 문으로 돌면서
    # td 라는 태그 class 는 method 이며 텍스트만 추출한다 / replace 를 통해 원하는 텍스트만 추출
    method=item.find("td",{"class":"method"}).text.replace("lecturehow","")
    aboutexam=item.find("td",{"class":"aboutexam"}).text.replace("test","")
    print("method : " + method + " \naboutexam : " + aboutexam) #  출력