import requests #pip install requests
from bs4 import BeautifulSoup #pip install beautifulsoup4

def main(ISIN):
    href = "https://www.gpw.pl/spolka?isin="+ ISIN
    html = requests.get(href)
    htmlDoc = html.text
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    shareData = {}
    shareData.update({"price" : soup.find("span", {"class" : "summary"}).text})
    
    return shareData
#print(main("PLALIOR00045")["price"])