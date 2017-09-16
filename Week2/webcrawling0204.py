import requests
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.3','Content-Type': 'application/json; charset=utf-8','Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}

r=requests.get("https://pythonprogramming.net/parsememcparseface",headers=headers)

c=r.content
soup=BeautifulSoup(c,"html.parser")


all=soup.find("p", {"class": "jstest"})
print(all)