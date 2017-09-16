import requests,operator,pandas,glob2
from bs4 import BeautifulSoup
from datetime import datetime
from bkcharts import Scatter, output_file, show


def crawlingComment(url,beginPage,endPage):

    l=[]
    d = {}
    now = datetime.now()

    # total page processing

    for pageCount in range(int(beginPage),int(endPage)):

        url="https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_politics&pool=cbox5&_callback=jQuery17005007762565150675_1503340099957&lang=ko&country=KR&objectId=news003%2C0008136468&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&page=" + str(pageCount) + "&sort=FAVORITE&current=1042698005&prev=1042485105&includeAllStatus=true&_=1503340179475"
        headers = {'referer': 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=001&aid=0008136468&isYeonhapFlash=Y&rc=N&m_view=1&includeAllCount=true'}
        jsons = requests.get(url,headers=headers)
        contents=str(BeautifulSoup(jsons.content,"html.parser"))
        l=contents.split('"contents":"')

        commentCount=l[0].split('count":{"comment":')[1].split(",")[0]
        replyCount=l[0].split('"reply":')[1].split(",")[0]


        for i in range(0,len(l)):

            if(i>1):

                commentContent=l[i].split('","userIdNo":"')[0]

                if commentContent is not "":

                    commentCode=l[i].split('userIdNo":"')[1].split('"')[0]
                    commentUser=l[i].split('userName":"')[1].split('"')[0]

                    d["commentUser"]=commentUser
                    d["commentCode"]=commentCode
                    d["commentContent"]=commentContent
                    print(commentContent + " / " + commentUser + " / " + commentCode)
                    l.append(d)

        print(l)
    df = pandas.DataFrame(l)
    df.to_csv('%s-%s-%s-%s-%s-%s.csv' % (now.year, now.month, now.day, now.hour, now.minute, now.second),
                  encoding='utf-8-sig', index=False)
    print("Success Get DataFIle and Save Data")


def crawlingData(date, pageCount):
    now = datetime.now()
    l=[]
    for pagecount in range(0,int(pageCount)):
        r = requests.get("http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100&date=" + str(date) + "&page=" + str(pagecount))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        all = soup.find_all("li")

        for item in all:
            for item2 in item.find_all("dl"):
                d = {}
                try:
                    linkTag = item2.find("dt", {"class": ""}).find("a")
                    d["LinkSrc"]=linkTag['href']
                    d["Title"]=linkTag.text.replace("\t", "").replace("\n", "").replace(",","").replace('"',"").replace("\r","")[1:len(linkTag.text) + 1]
                except:
                    d["LinkSrc"]="None"
                    d["Title"]="None"

                try:
                    contentTag = item2.find("dd")
                    d["Content"]=contentTag.text.replace("\t","").replace("\n","").replace("\r","").replace(",","").replace('"',"").split("…")[0]
                    d["Company"]=contentTag.find("span",{"class":"writing"}).text
                    d["Date"]=contentTag.find("span", {"class": "date"}).text
                except:
                    d["Content"]="None"
                    d["Company"]="None"
                    d["Date"]="None"

                try:
                    imgTag = item2.find("dt", {"class": "photo"}).find("img")
                    d["imgSrc"]=imgTag["src"]
                except:
                    d["imgSrc"] = "No image"

                l.append(d)

    df = pandas.DataFrame(l)

    df.to_csv('%s-%s-%s-%s-%s-%s.csv' % ( now.year, now.month, now.day,now.hour, now.minute, now.second ), encoding='utf-8-sig',index=False)
    print("Success Get DataFIle and Save Data")


def loadFile(fileName):
    now = datetime.now()
    if len(glob2.glob("*.csv"))== 0:
        print("No file found this directory")
        return -1
    else :

        if fileName=="all":
            result=[]
            for i in glob2.glob("*.csv"):
                result.append(pandas.read_csv(i))


            outputFileName = '%s-%s-%s-%s-%s-%s merging.csv' % (
            now.year, now.month, now.day, now.hour, now.minute, now.second)

            resultDf = pandas.concat(result,ignore_index=True)

            resultDf.to_csv(outputFileName, encoding='utf-8-sig')
            return outputFileName

        else :
            return fileName




def analyzeFile(fileName):


    outputFileName=loadFile(fileName)

    if outputFileName is not -1:

        df = pandas.read_csv(outputFileName)
        content = list(df["Content"])
        title = list(df["Title"])
        company = list(df["Company"])

        contentDic=dict()
        titleDic=dict()


        rankWord(content,contentDic)
        rankWord(title,titleDic)

        sortedTitleWord=sorted(titleDic.items(), key=operator.itemgetter(1),reverse=True)
        sortedContentWord = sorted(contentDic.items(), key=operator.itemgetter(1),reverse=True)

        sortedContentWordDic=dict(sortedContentWord)
        contentDf = pandas.DataFrame()
        contentDf['Word'] = sortedContentWordDic.keys()
        contentDf['WordCount'] = sortedContentWordDic.values()
        print(contentDf)
        print(len(sortedContentWordDic))


        sortedTitleWordDic=dict(sortedTitleWord)
        titleDf = pandas.DataFrame()
        titleDf['Word'] = sortedTitleWordDic.keys()
        titleDf['WordCount'] = sortedTitleWordDic.values()
        print(titleDf)
        print(len(sortedTitleWordDic))
        p=Scatter(titleDf,x="Word",y="WordCount",title="Title Word list ",xlabel="Words",ylabel="Word Count")
        output_file("analyze.html")
        show(p)

def rankWord(wordList,wordDic):

    contentSplit=list()
    for splitContentWord in wordList:
        if splitContentWord is not None:
            for i in splitContentWord.split():
                if noum(i) is not "a":
                    contentSplit.append(noum(i))

    for word in contentSplit:
        if word not in wordDic:
            wordDic[word] = 1
        else:
            wordDic[word] = wordDic[word] + 1

def noum(word):
    word=word.replace("[", "").replace(".", "").replace("]", "").replace("'","").replace('"',"").replace("{","").replace("}","").replace(")","").replace("=","")
    word=word.replace("은","").replace("는","").replace("이","").replace("가","").replace("【","").replace("】","").replace("“","").replace("을","").replace("를","")
    word=word.replace("◀","").replace("▶","").replace(")","").replace("◆","").replace("-","").replace("/","").replace("@","").replace("”","").replace("“","")
    word=word.replace("기자","").replace("■","").replace("에","").replace("앵커","")

    if word is "":
        return "a"

    return word


def mainSetting():
    while(1):
        kb=input("$ ")
        if kb=="exit":
            break
        elif kb=="crawling":
            date=input("Enter news date : ")
            page = input("Enter your pageCount : ")
            crawlingData(date, page)
        elif kb=="loadAll":
            analyzeFile("all")
        elif kb=="load":
            fileName=input("Enter your csv file name : ")
            analyzeFile(fileName)
        else :
            print("command error")

crawlingComment(9,1,5)
# mainSetting()