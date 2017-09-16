import requests, operator, pandas, glob2
from bs4 import BeautifulSoup
from datetime import datetime


def crawlingData(date, pageCount):
    now = datetime.now()
    l = []
    for pagecount in range(0, int(pageCount)):
        r = requests.get(
            "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100&date=" + str(date) + "&page=" + str(
                pagecount))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        all = soup.find_all("li")

        for item in all:
            for item2 in item.find_all("dl"):
                d = {}
                try:
                    linkTag = item2.find("dt", {"class": ""}).find("a")
                    d["LinkSrc"] = linkTag['href']
                    d["Title"] = linkTag.text.replace("\t", "").replace("\n", "").replace(",", "").replace('"',
                                                                                                           "").replace(
                        "\r", "")[1:len(linkTag.text) + 1]
                except:
                    d["LinkSrc"] = "None"
                    d["Title"] = "None"

                try:
                    contentTag = item2.find("dd")
                    d["Content"] = \
                    contentTag.text.replace("\t", "").replace("\n", "").replace("\r", "").replace(",", "").replace('"',
                                                                                                                   "").split(
                        "…")[0]
                    d["Company"] = contentTag.find("span", {"class": "writing"}).text
                    d["Date"] = contentTag.find("span", {"class": "date"}).text
                except:
                    d["Content"] = "None"
                    d["Company"] = "None"
                    d["Date"] = "None"

                try:
                    imgTag = item2.find("dt", {"class": "photo"}).find("img")
                    d["imgSrc"] = imgTag["src"]
                except:
                    d["imgSrc"] = "No image"

                l.append(d)

    df = pandas.DataFrame(l)

    df.to_csv('%s-%s-%s-%s-%s-%s.csv' % (now.year, now.month, now.day, now.hour, now.minute, now.second),
              encoding='utf-8-sig', index=False)
    print("Success Get DataFIle and Save Data")


def loadFile(fileName):
    outputFileName = checkFileName(fileName)

    if outputFileName is not -1:
        df = pandas.read_csv(outputFileName)
        content = df["Content"]
        title = df["Title"]
        company = df["Company"]

        print("csv FIle Load Success")
    else:
        print("Error csv File")


def checkFileName(fileName):
    now = datetime.now()
    if len(glob2.glob("*.csv")) == 0:
        print("No file found in this directory")
        return -1
    else:

        if fileName == "all":
            result = []
            for i in glob2.glob("*.csv"):
                result.append(pandas.read_csv(i))

            outputFileName = '%s-%s-%s-%s-%s-%s merging.csv' % (
                now.year, now.month, now.day, now.hour, now.minute, now.second)

            resultDf = pandas.concat(result, ignore_index=True)
            resultDf.to_csv(outputFileName, encoding='utf-8-sig')
            return outputFileName

        else:
            return fileName


def mainSetting():
    while (1):
        kb = input("$ ")
        if kb == "exit":
            break
        elif kb == "crawling":
            date = input("Enter news date : ")
            page = input("Enter your pageCount : ")
            crawlingData(date, page)
        elif kb == "loadAll":
            loadFile("all")
        elif kb == "load":
            fileName = input("Enter your csv file name : ")
            loadFile(fileName)
        else:
            print("command error")


mainSetting()