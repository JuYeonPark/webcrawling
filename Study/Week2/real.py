import requests
from bs4 import BeautifulSoup


# 사용자로부터 키워드를 입력받고, 키워드를 검색해서(네이버) 뉴스에 접속한 다음 덧글을 크롤링 해오기

headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'referer':'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=001&aid=0009572260&isYeonhapFlash=Y&rc=N&m_view=1&includeAllCount=true&m_url=%2Fcomment%2Fall.nhn%3FserviceId%3Dnews%26gno%3Dnews001%2C0009572260%26sort%3Dlikability'
}

r=requests.get("https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_politics&pool=cbox5&_callback=jQuery17023240944630416482_1506390886908&lang=ko&country=&objectId=news001%2C0009572260&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&page=2&sort=FAVORITE&current=1079250985&prev=1079229065&includeAllStatus=true&_=1506390900990",headers=headers)
c=r.content

soup=BeautifulSoup(c,"html.parser")

print(soup)

