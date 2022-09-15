import requests
import shutil
import pymysql
import time
import hashlib
import os
import PyPDF2
import olefile
from bs4 import BeautifulSoup

class Headers:
    #menuNo : 200476(검사결과제재)
    #pageInex : 페이지번호
    #sdate : 시작일시(YYYY-MM-DD)
    #edate : 종료일시(YYYY-MM-DD)
    #searchCnd : 3(전체),2(금융회사명),1(제재조치요구사항내용)
    #searchWrd : urlencoded 검색어
    def __init__(self,url,sdate="-".join((time.strftime("%Y"),"01","01"))):
        self.url = url
        self.__params = {
            "menuNo" :200476,
            "pageIndex":1,
            "sdate" : sdate,
            "edate" : time.strftime("%Y-%m-%d"),
            "searchCnd":3,
            "searchWrd":""
        }
    
    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self,k,v):
        self.__params[k] = v


def download_file(url,fname="",path="./"):
    if fname == "":
        fname = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(os.path.join(path,fname), 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return fname

class pdfExtractor:
    law = ["신용정보","정보통신","전자금융","개인정보"]
    flag = False
    def __init__(self,fname):
        self.fname = fname
        if self.extract(fname):
            self.flag = True

    def extract(self,fname):
        pdf = PyPDF2.PdfFileReader(fname)
        for i in range(len(pdf.pages)):
            text = pdf.pages[i].extractText()
            for law in self.law:
                if text.find(law) >=0:
                    return True
        return False

class hwpExtractor:
    law = ["신용정보","정보통신","전자금융","개인정보"]
    flag = False
    def __init__(self,fname):
        self.fname = fname
        if self.extract(fname):
            self.flag = True

    def extract(self,fname):
        fname = olefile.OleFileIO(fname)
        #PrvText 스트림 내의 내용을 읽기
        encoded_text = fname.openstream("PrvText").read() 
        #인코딩된 텍스트를 UTF-16으로 디코딩
        decoded_text = encoded_text.decode("UTF-16")
        for law in self.law:
                if decoded_text.find(law) >=0:
                    return True
        return False


if __name__ == "__main__":
    base_url = "https://www.fss.or.kr"
    entry_url = "/fss/job/openInfo/list.do?"
    fssHeaders = Headers(base_url+entry_url,sdate="2018-01-01")
    while True:
        res=requests.get(fssHeaders.url,params=fssHeaders.params).text
        
        soup = BeautifulSoup(res,'html.parser')
        tags = soup.find_all("a",class_="b-default xs")
        for tag in tags:
            new_url = "/".join((base_url,"/".join(entry_url.split("/")[1:-1]),tag["href"][2:]))
            print(new_url)
            soup=BeautifulSoup(requests.get(new_url).text,'html.parser')
            pdfurl = soup.find("div",class_="file-list__set__item").a["href"]
            fname = soup.find("span",class_="name").text
            fname = download_file("/".join((base_url,pdfurl)),fname)
            if fname.split(".")[-1] == "pdf":
                isContains = pdfExtractor(fname).flag
            else:
                isContains = hwpExtractor(fname).flag
                
            if isContains:
                #hash
                #save to MySQL
                continue
            else:
                os.remove(fname)
        fssHeaders.params["pageIndex"] +=1