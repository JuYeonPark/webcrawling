import requests
from bs4 import BeautifulSoup

# Week1 / 1주차 참고
r=requests.get("http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100")
c=r.content
soup=BeautifulSoup(c,"html.parser")

# ul 이며 class 는 type06_headline 태그를 찾는다
all=soup.find("ul",{"class":"type06_headline"})

# 이미지 주소 가져오는 함수
def getImageSrc():
    dl=all.find_all("dl") # dl 태그를 모두 찾는다
    for item2 in dl:
        try: # 에러가 없을 시(dl태그를 찾을 시)
            # 찾은 dl태그중에서 dt 태그(class :photo) 를 찾고 다시 그 안에서 img 태그를 찾는다
            img=item2.find("dt",{"class":"photo"}).find("img")
            # 찾은 img 태그 중 속성 'src'의 내용을 가져와 출력한다.
            print(img['src'])
        except :
            # 에러 발생시(dl 태그 존재 안함)
            print("No image")

# 주소와 기사제목을 가져오는 함수
def getLinkAndTitle():
    dl = all.find_all("dl")
    for item2 in dl:
        link = item2.find("dt",{"class":""}).find("a")
        print(link['href'])
        # replace를 통해서 탭,줄띄움을 모두 공백으로 바꾸고
        # 문장들 중 첫번째 자리(스페이스)를 짤라낸다
        print(link.text.replace("\t","").replace("\n","")[1:len(link.text)+1])


# 기사내용을 가져오는 함수
def getContent ():
    dl = all.find_all("dl")
    for item2 in dl:
        try:
            content = item2.find("dd")
            print(content.text.replace("\t","").replace("\n","").split("...")[0])
            print(content.find("span",{"class":"writing"}).text)
            print(content.find("span", {"class": "date"}).text)
        except:
            print("No Content")

# 함수 호출
getContent()
