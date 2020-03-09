from time import sleep as delay
import requests
from bs4 import BeautifulSoup as bs


def scraper():
    r = requests.get('https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html')
    page = r.text
    soup = bs(page, 'lxml')


    f = open('cdc-date.txt', 'r')
    date = f.read()
    f.close()

    dates = soup.find_all(attrs={'class':'text-red'})
    pageDate = dates[0].text

    if pageDate != date:

        fnew = open('cdc-date.txt', 'w')
        fnew.write(pageDate)
        fnew.close()

        litags = soup.find_all('li')
        cases = litags[11].text
        deaths = litags[12].text
        statesWith = litags[13].text


#while True:
    #delay(60*30)
if True:
    scraper()