import requests
from bs4 import BeautifulSoup

r=requests.get("http://lambutan.dothome.co.kr/")
c=r.content
soup=BeautifulSoup(c,"html.parser")


all=soup.find("tbody")
all2=all.find_all("tr",{"class":""})

for item in all2:
    professor=item.find("td",{"class":"professor"}).text
    lectureName=item.find("td",{"class":"lecture"}).text
    orther=item.find("td",{"class":"orther"}).text
    grade = item.find("td", {"class": "grade"}).text
    evaluation=item.find("td", {"class": "evaluation"}).text
    print(professor + " / " + lectureName + " / " + orther + " / " + grade + " / " + evaluation)