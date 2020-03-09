import requests
from bs4 import BeautifulSoup as bs
from time import sleep as delay
from secret import *
from smtplib import SMTP
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def findValue(str):
    temp = [int(s) for s in str.split() if s.isdigit()]
    return temp[0]


def scraper():
    r = requests.get('https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html')
    page = r.text
    soup = bs(page, 'lxml')


    f = open('cdc-date.txt', 'r')
    date = f.readlines()
    f.close()

    dates = soup.find_all(attrs={'class':'text-red'})
    pageDate = dates[0].text

    if pageDate != date[0]:

        fnew = open('cdc-date.txt', 'w')
        fnew.write(pageDate)

        div = soup.find(attrs={'class':'card-body bg-white'})

        litags = div.find_all('li')
        cases = litags[0].text
        deaths = litags[1].text
        statesWith = litags[2].text

        fnew.write(f'\n{cases}')
        fnew.write(f'\n{deaths}')
        fnew.write(f'\n{statesWith}')
        fnew.close()

        nowFormatted = datetime.now().strftime('%-m/%-d/%y %-I:%M %p')

        currentCases = findValue(cases)
        currentDeaths = findValue(deaths)
        currentStates = findValue(statesWith)
        pastCases = findValue(date[1])
        pastDeaths = findValue(date[2])
        pastStates = findValue(date[3])

        if currentCases > pastCases:
            casesPercentage = ((currentCases - pastCases) / pastCases) * 100
            changeCases = 'increase'
        else:
            casesPercentage = ((pastCases - currentCases) / pastCases) * 100
            changeCases = 'decrease'

        if currentDeaths > pastDeaths:
            deathsPercentage = ((currentDeaths - pastDeaths) / pastDeaths) * 100
            changeDeaths = 'increase'
        else:
            deathsPercentage = ((pastDeaths - currentDeaths) / pastDeaths) * 100
            changeDeaths = 'decrease'

        if currentStates > pastStates:
            statesPercentage = ((currentStates - pastStates) / pastStates) * 100
            changeStates = 'increase'
        else:
            statesPercentage = ((pastStates - currentStates) / pastStates) * 100
            changeStates = 'decrease'

        email_message = (f'''
Hello,

Update: {nowFormatted}

CDC {pageDate}

{cases}
{casesPercentage}% {changeCases} in cases in U.S.

{deaths}
{deathsPercentage}% {changeDeaths} in deaths in U.S.

{statesWith}
{statesPercentage}% {changeStates} in states with cases in U.S.

- COVID-19 Reporter
                          ''')

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

    #r = requests.get('https://projects.sfchronicle.com/2020/coronavirus-map/')
    #page = r.text


while True:
    scraper()
    delay(60*60)