import requests
from bs4 import BeautifulSoup as bs
from time import sleep as delay
from secret import *
from smtplib import SMTP
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def findValue(str):

    string = ''

    for letter in list(str):
        if letter.isdigit():
            string += letter

    return float(string)

def findValueList(listA):

    for items in listA:
        if items.isdigit():
            return float(items)


def scraper():
    r = requests.get('https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html')
    page = r.text
    soup = bs(page, 'lxml')


    f = open('cdc-date.txt', 'r')
    data = f.readlines()
    f.close()

    fo = open('cdc.txt', 'r')
    date = fo.read()

    dates = soup.find_all(attrs={'class':'text-red'})
    pageDate = dates[0].text

    if pageDate != date:

        fnew = open('cdc.txt', 'w')
        fnew.write(pageDate)
        fnew.close()

        div = soup.find(attrs={'class':'card-body bg-white'})

        litags = div.find_all('li')
        cases = litags[0].text
        deaths = litags[1].text
        statesWith = litags[2].text

        fnew = open('cdc-date.txt', 'w')

        fnew.write(cases)
        fnew.write(f'\n{deaths}')
        fnew.write(f'\n{statesWith}')
        fnew.close()

        nowFormatted = datetime.now().strftime('%-m/%-d/%y %-I:%M %p')

        currentCases = findValue(cases)
        currentDeaths = findValue(deaths)
        currentStates = findValueList(statesWith.split(' '))
        pastCases = findValue(data[0])
        pastDeaths = findValue(data[1])
        pastStates = findValueList(data[2].split(''))

        if currentCases > pastCases:
            differenceCases = currentCases - pastCases
            casesPercentage = (differenceCases / pastCases) * 100
            changeCases = 'increase'
        else:
            differenceCases = pastCases - currentCases
            casesPercentage = (differenceCases / pastCases) * 100
            changeCases = 'decrease'

        if currentDeaths > pastDeaths:
            differenceDeaths = currentDeaths - pastDeaths
            deathsPercentage = (differenceDeaths / pastDeaths) * 100
            changeDeaths = 'increase'
        else:
            differenceDeaths = pastDeaths - currentDeaths
            deathsPercentage = (differenceDeaths / pastDeaths) * 100
            changeDeaths = 'decrease'

        if currentStates > pastStates:
            differenceStates = currentStates - pastStates
            statesPercentage = (differenceStates / pastStates) * 100
            changeStates = 'increase'
        else:
            differenceStates = pastStates - currentStates
            statesPercentage = (differenceStates / pastStates) * 100
            changeStates = 'decrease'

        email_message = (f'''
Hello,

Update: {nowFormatted}

CDC {pageDate}

Current Cases: {cases}
{int(differenceCases)} case {changeCases}.
{casesPercentage}% {changeCases} in cases in U.S.

Current Death count: {deaths}
{int(differenceDeaths)} death {changeDeaths}.
{deathsPercentage}% {changeDeaths} in deaths in U.S.

Current States reporting cases: {statesWith}
{int(differenceStates)} state {changeStates}.
{statesPercentage}% {changeStates} in states with cases in U.S.

- COVID-19 Reporter''')

        msg = MIMEMultipart()
        msg['From'] = f'COVID-19 Reporter <{senderEmail}>'
        msg['To'] = recieverEmail
        msg['Subject'] = f'Update: {nowFormatted}'
        msg.attach(MIMEText(email_message,'plain'))
        message = msg.as_string()

        smtp_server = SMTP('smtp.gmail.com', 587)
        smtp_server.ehlo_or_helo_if_needed()
        smtp_server.starttls()
        smtp_server.ehlo_or_helo_if_needed()
        smtp_server.login(senderEmail, senderPassword)
        smtp_server.sendmail(senderEmail, recieverEmail, message)
        smtp_server.quit()

        print(f'Email sent @ {nowFormatted}')

#if True:
while True:
    scraper()
    delay(60*30)