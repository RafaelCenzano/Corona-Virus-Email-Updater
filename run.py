import requests
import json
import os
from bs4 import BeautifulSoup as bs
from secret import *
from smtplib import SMTP
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def scraper():
    r = requests.get('https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html')
    page = r.text
    soup = bs(page, 'lxml')

    nowFormatted = datetime.now().strftime('%-m/%-d/%y %-I:%M %p')

    totals = soup.find_all(attrs={'class':'count'})
    newCasesData = soup.find_all(attrs={'class':'new-cases'})

    newCasesText = newCasesData[0].text
    newCases = newCasesText[:len(newCasesText)-11]
    newDeathsText = newCasesData[1].text
    newDeaths = newDeathsText[:len(newDeathsText)-12]

    r2 = requests.get('https://www.sfchronicle.com/bayarea/article/Coronavirus-live-updates-news-bay-area-15237940.php')
    page2 = r2.text
    soup2 = bs(page2, 'lxml')

    pTags = soup2.findAll('p')

    californiaParts = pTags[3].text[3:].split()
    californiaCases = californiaParts[0]
    californiaDeaths = californiaParts[len(californiaParts)-2]

    bayAreaParts = pTags[4].text[2:].split()
    bayAreaCases = bayAreaParts[0]
    bayAreaDeaths = bayAreaParts[len(bayAreaParts)-2]

    calCasesToday = int(''.join(californiaCases.split(',')))
    calDeathsToday = int(''.join(californiaDeaths.split(',')))
    baCasesToday = int(''.join(bayAreaCases.split(',')))
    baDeathsToday = int(''.join(bayAreaDeaths.split(',')))

    if os.path.isfile('past.json') == False:

        jsonData = {'calCasesToday':calCasesToday, 'calDeathsToday':calDeathsToday, 'baCasesToday':baCasesToday, 'baDeathsToday':baDeathsToday}

        with open('past.json', 'w') as jsonFile:
            json.dump(jsonData, jsonFile)

        calDifferenceCases = 'Unknown'
        calDifferenceDeaths = 'Unknown'
        baDifferenceCases = 'Unknown'
        baDifferencesDeaths = 'Unknown'

    else:

        with open('past.json', 'r') as jsonFile:
            jsonData = json.load(jsonFile)

        calDifferenceCases = calCasesToday - jsonData['calCasesToday']
        calDifferenceDeaths = calDeathsToday - jsonData['calDeathsToday']
        baDifferenceCases = baCasesToday - jsonData['baCasesToday']
        baDifferencesDeaths = baDeathsToday - jsonData['baDeathsToday']


    email_message = (f'''
Hello,

Update: {nowFormatted}


United States Data from CDC:

Total cases: {totals[0].text}
New cases: {newCases}

Total deaths: {totals[1].text}
New deaths: {newDeaths}


California Data from SF Chronicle:

Total cases: {californiaCases}
New cases: {calDifferenceCases}

Total deaths: {californiaDeaths}
New deaths: {calDifferenceDeaths}


San Francisco from SF Chronicle:

Total cases: {bayAreaCases}
New cases: {baDifferenceCases}

Total deaths: {bayAreaDeaths}
New deaths: {baDifferencesDeaths}


- COVID-19 Reporter''')

    for recieverEmail in recieverEmails:

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

        print(f'Email sent to {recieverEmail} @ {nowFormatted}')

if __name__ == '__main__':
    scraper()