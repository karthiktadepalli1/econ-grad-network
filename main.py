from bs4 import BeautifulSoup
import requests
import re

# essentially get every page from every profiles and results thread
# keep a single url list for all of the pages
# keep a single details list for all of the profiles across all pages
# make an object for each profile
"""
class Applicant():
    def __init__(self, profileDict):
        self.profile = profileDict
        self.accept = profileDict['Acceptances'].strip().split(",")
        for element in self.accept:
            element = element.strip()
        self.wait = profileDict['Waitlists'].strip().split(",")
        for element in self.wait:
            element = element.strip()
        self.reject = profileDict['Rejections'].strip().split(",")
        for element in self.reject:
            element = element.strip()
"""


def getDetails(urlList):
    detailsList = []
    for url in urlList:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for profile in soup.find_all('blockquote'):
            details = profile.get_text().split("\r\n")
            profileDict = {}
            for detail in details:
                detail = detail.split(":")
                if len(detail) == 2:
                    profileDict[detail[0]] = detail[1]
            detailsList.append(profileDict)

    return detailsList


def getAllPages(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for element in soup.find_all('a', attrs={'href': 'javascript://'}):
        text = element.get_text()
        if "Page" in text:
            numPages = int(text.split(" ")[-1])

    urlList = []
    urlList.append(url)
    if numPages > 1:
        for num in range(2, numPages+1):
            newurl = url[:-5] + "-" + str(num) + url[-5:]
            urlList.append(newurl)

    return urlList


def cleanName(someName):
    split = someName.strip().split(" ")
    for element in split:
        if element == "":
            i = split.index(element)
            del split[i]
    someName = " ".join(split)
    print(someName)
    return(someName)


def cleanAllNames(string):
    string = re.sub(r"\([^)]+\)", "", string).strip()
    test = string.split(" ")
    split = string.split(",")
    if len(test) > 3 and len(split) == 1:
        split = string.split(";")
    cleanSplit = [cleanName(element) for element in split]
    print(cleanSplit)
    return(cleanSplit)


link = "http://www.urch.com/forums/phd-economics/160036-profiles-results-2018-a.html"
listt = getAllPages(link)
dets = getDetails(listt)
del dets[0]

print(dets)
