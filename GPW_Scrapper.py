import requests #pip install requests
from bs4 import BeautifulSoup #pip install beautifulsoup4
import time

def main(symbol):
    href = "https://www.gpw.pl/wyniki-wyszukiwania?search=1&search_lang=PL&search="+ symbol
    html = requests.get(href)
    htmlDoc = html.text
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    for a in soup.find_all('a', href=True):
        if 'spolka' in a['href']:
            href = "https://www.gpw.pl/"+a['href']
            isin = a['href'][-12:]
            html = requests.get(href)
            htmlDoc = html.text
            soup = BeautifulSoup(htmlDoc, 'html.parser')
            break
    shareData = {}
    shareData.update({"symbol" : soup.find("input", {"id" : "glsSkrot"}).get("value").strip()})
    shareData.update({"price" : soup.find("span", {"class" : "summary"}).text})
    shareData.update({"ISIN" : isin})
    
    timeNow = time.localtime()
    dateNow = str(timeNow.tm_mday) + "." + str(timeNow.tm_mon) + "." + str(timeNow.tm_year)
    shareData.update({"date" : dateNow})
    return shareData
