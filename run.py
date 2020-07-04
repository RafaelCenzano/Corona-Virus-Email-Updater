import requests
import json
import os
from bs4 import BeautifulSoup as bs
from secret import *
from smtplib import SMTP
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def maths(num1, num2, num3=None):
    num1 = int(''.join(num1.split(',')))
    num2 = int(''.join(num2.split(',')))
    if num3:
        num3 = int(''.join(num3.split(',')))
        num = '{:,}'.format(num1 - num2 - num3)
    else:
        num = '{:,}'.format(num1 - num2)
    return num


def scraper():
    r = requests.get(
        'https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html')
    page = r.text
    soup = bs(page, 'lxml')

    nowFormatted = datetime.now().strftime('%-m/%-d/%y %-I:%M %p')

    totals = soup.findAll(attrs={'class': 'count'})
    newCasesData = soup.findAll(attrs={'class': 'new-cases'})

    newCasesText = newCasesData[0].text
    newCases = newCasesText[:len(newCasesText) - 11]
    newDeathsText = newCasesData[1].text
    newDeaths = newDeathsText[:len(newDeathsText) - 12]

    r2 = requests.get(
        'https://www.sfchronicle.com/bayarea/article/Coronavirus-live-updates-news-bay-area-15237940.php')
    page2 = r2.text
    soup2 = bs(page2, 'lxml')

    pTags = soup2.findAll('p')

    californiaParts = pTags[3].text[2:].split()
    californiaCases = californiaParts[0]
    californiaDeaths = californiaParts[len(californiaParts) - 2]

    bayAreaParts = pTags[4].text[2:].split()
    bayAreaCases = bayAreaParts[0]
    bayAreaDeaths = bayAreaParts[len(bayAreaParts) - 2]

    with open(jsonFilePath, 'r') as jsonFile:
        jsonDataRead = json.load(jsonFile)

    try:
        calCasesToday = int(''.join(californiaCases.split(',')))
    except BaseException:
        calCasesToday = jsonDataRead['calCasesToday']

    try:
        calDeathsToday = int(''.join(californiaDeaths.split(',')))
    except BaseException:
        calDeathsToday = jsonDataRead['calDeathsToday']

    try:
        baCasesToday = int(''.join(bayAreaCases.split(',')))
    except BaseException:
        baCasesToday = jsonDataRead['baCasesToday']
        bayAreaCases = jsonDataRead['baCasesToday']

    try:
        baDeathsToday = int(''.join(bayAreaDeaths.split(',')))
    except BaseException:
        baDeathsToday = jsonDataRead['baDeathsToday']
        bayAreaDeaths = jsonDataRead['baDeathsToday']

    r3 = requests.get('https://www.worldometers.info/coronavirus/')
    page3 = r3.text
    soup3 = bs(page3, 'lxml')

    spanTags = soup3.findAll('span')
    totalsWorld = soup3.findAll('div', attrs={'class': 'number-table-main'})

    worldCases = spanTags[4].text
    worldDeaths = spanTags[5].text
    worldRecoveries = spanTags[6].text
    mildCasesWorld = spanTags[8].text
    criticalCasesWorld = spanTags[9].text
    recoveredWorld = spanTags[11].text
    currentWorldCases = totalsWorld[0].text
    currentWorldClosed = totalsWorld[1].text

    worldCasesToday = int(''.join(worldCases.split(',')))
    worldDeathsToday = int(''.join(worldDeaths.split(',')))
    worldRecoveriesToday = int(''.join(worldRecoveries.split(',')))

    if os.path.isfile(jsonFilePath) == False:

        jsonData = {
            'other': {
                'currentWorldCases': currentWorldCases,
                'uscases': totals[0].text,
                'usnewcases': newCases,
                'usenewdeaths': newDeaths,
                'usdeaths': totals[1].text},
            'past': {
                'calCasesToday': calCasesToday,
                'calDeathsToday': calDeathsToday,
                'baCasesToday': baCasesToday,
                'baDeathsToday': baDeathsToday,
                'worldCases': worldCasesToday,
                'worldDeaths': worldDeathsToday,
                'worldRecoveries': worldRecoveriesToday},
            'past2': {
                'calCasesToday': calCasesToday,
                'calDeathsToday': calDeathsToday,
                'baCasesToday': baCasesToday,
                'baDeathsToday': baDeathsToday,
                'worldCases': worldCasesToday,
                'worldDeaths': worldDeathsToday,
                'worldRecoveries': worldRecoveriesToday}}

        with open(jsonFilePath, 'w') as jsonFile:
            json.dump(jsonData, jsonFile)

        calDifferenceCases = 'Unknown'
        calDifferenceDeaths = 'Unknown'
        baDifferenceCases = 'Unknown'
        baDifferencesDeaths = 'Unknown'
        wDifferenceCases = 'Unknown'
        wDifferenceDeath = 'Unknown'
        wDifferenceRecoveries = 'Unknown'

        calDifferenceCases1 = 'Unknown'
        calDifferenceDeaths1 = 'Unknown'
        baDifferenceCases1 = 'Unknown'
        baDifferencesDeaths1 = 'Unknown'
        wDifferenceCases1 = 'Unknown'
        wDifferenceDeath1 = 'Unknown'
        wDifferenceRecoveries1 = 'Unknown'

    else:

        with open(jsonFilePath, 'r') as jsonFile:
            jsonDataFile = json.load(jsonFile)

        calDifferenceCases = '{:,}'.format(
            calCasesToday - jsonDataFile['past']['calCasesToday'])
        calDifferenceDeaths = '{:,}'.format(
            calDeathsToday - jsonDataFile['past']['calDeathsToday'])
        baDifferenceCases = '{:,}'.format(
            baCasesToday - jsonDataFile['past']['baCasesToday'])
        baDifferencesDeaths = '{:,}'.format(
            baDeathsToday - jsonDataFile['past']['baDeathsToday'])
        wDifferenceCases = '{:,}'.format(
            worldCasesToday - int(jsonDataFile['past']['worldCases']))
        wDifferenceDeath = '{:,}'.format(
            worldDeathsToday - int(jsonDataFile['past']['worldDeaths']))
        wDifferenceRecoveries = '{:,}'.format(
            worldRecoveriesToday - int(jsonDataFile['past']['worldRecoveries']))

        calDifferenceCases1 = '{:,}'.format(
            jsonDataFile['past']['calCasesToday'] -
            jsonDataFile['past2']['calCasesToday'])
        calDifferenceDeaths1 = '{:,}'.format(
            jsonDataFile['past']['calDeathsToday'] -
            jsonDataFile['past2']['calDeathsToday'])
        baDifferenceCases1 = '{:,}'.format(
            jsonDataFile['past']['baCasesToday'] -
            jsonDataFile['past2']['baCasesToday'])
        baDifferencesDeaths1 = '{:,}'.format(
            jsonDataFile['past']['baDeathsToday'] -
            jsonDataFile['past2']['baDeathsToday'])
        wDifferenceCases1 = '{:,}'.format(
            jsonDataFile['past']['worldCases'] - int(jsonDataFile['past2']['worldCases']))
        wDifferenceDeath1 = '{:,}'.format(
            jsonDataFile['past']['worldDeaths'] - int(jsonDataFile['past2']['worldDeaths']))
        wDifferenceRecoveries1 = '{:,}'.format(
            jsonDataFile['past']['worldRecoveries'] - int(jsonDataFile['past2']['worldRecoveries']))

        pastWorldCases = jsonDataFile['other']['currentWorldCases']
        pastUsCases = jsonDataFile['other']['uscases']
        pastUsNewCases = jsonDataFile['other']['usnewcases']
        pastUsDeaths = jsonDataFile['other']['usdeaths']
        pastUsNewDeaths = jsonDataFile['other']['usenewdeaths']

        jsonDataFile['past2']['calCasesToday'] = jsonDataFile['past']['calCasesToday']
        jsonDataFile['past2']['calDeathsToday'] = jsonDataFile['past']['calDeathsToday']
        jsonDataFile['past2']['baCasesToday'] = jsonDataFile['past']['baCasesToday']
        jsonDataFile['past2']['baDeathsToday'] = jsonDataFile['past']['baDeathsToday']
        jsonDataFile['past2']['worldCases'] = jsonDataFile['past']['worldCases']
        jsonDataFile['past2']['worldDeaths'] = jsonDataFile['past']['worldDeaths']
        jsonDataFile['past2']['worldRecoveries'] = jsonDataFile['past']['worldRecoveries']

        jsonDataFile['past']['calCasesToday'] = calCasesToday
        jsonDataFile['past']['calDeathsToday'] = calDeathsToday
        jsonDataFile['past']['baCasesToday'] = baCasesToday
        jsonDataFile['past']['baDeathsToday'] = baDeathsToday
        jsonDataFile['past']['worldCases'] = worldCasesToday
        jsonDataFile['past']['worldDeaths'] = worldDeathsToday
        jsonDataFile['past']['worldRecoveries'] = worldRecoveriesToday

        jsonDataFile['other'] = {
            'currentWorldCases': currentWorldCases,
            'uscases': totals[0].text,
            'usnewcases': newCases,
            'usenewdeaths': newDeaths,
            'usdeaths': totals[1].text}

        with open(jsonFilePath, 'w') as jsonFile:
            json.dump(jsonDataFile, jsonFile)

    emailMessage = (f'''
Hello,

Update: {nowFormatted}


World Data from WorldOMeter:

Total cases since outbreak: {worldCases}, Yesterday: {maths(worldCases,wDifferenceCases)}
Total current cases: {currentWorldCases}, Yesterday: {pastWorldCases}
New cases: {wDifferenceCases}, Yesterday: {wDifferenceCases1}

Total closed cases: {currentWorldClosed}, Yesterday: {maths(currentWorldClosed,wDifferenceDeath,wDifferenceRecoveries)}
Total deaths: {worldDeaths}, Yesterday: {maths(worldDeaths,wDifferenceDeath)}
New deaths: {wDifferenceDeath}, Yesterday: {wDifferenceDeath1}
Total Recoveries: {worldRecoveries}, Yesterday: {maths(worldRecoveries,wDifferenceRecoveries)}
New Recoveries: {wDifferenceRecoveries}, Yesterday: {wDifferenceRecoveries1}


United States Data from CDC:

Total cases: {totals[0].text}, Yesterday: {pastUsCases}
New cases: {newCases}, Yesterday: {pastUsNewCases}

Total deaths: {totals[1].text}, Yesterday: {pastUsDeaths}
New deaths: {newDeaths}, Yesterday: {pastUsNewDeaths}


California Data from SF Chronicle:

Total cases: {californiaCases}, Yesterday: {maths(californiaCases,calDifferenceCases)}
New cases: {calDifferenceCases}, Yesterday: {calDifferenceCases1}

Total deaths: {californiaDeaths}, Yesterday: {maths(californiaDeaths,calDifferenceDeaths)}
New deaths: {calDifferenceDeaths}, Yesterday: {calDifferenceDeaths1}


Bay Area from SF Chronicle:

Total cases: {bayAreaCases}, Yesterday: {maths(bayAreaCases,baDifferenceCases)}
New cases: {baDifferenceCases}, Yesterday: {baDifferenceCases1}

Total deaths: {bayAreaDeaths}, Yesterday: {maths(bayAreaDeaths,baDifferencesDeaths)}
New deaths: {baDifferencesDeaths}, Yesterday: {baDifferencesDeaths1}


- COVID-19 Reporter
(Created by Rafael Cenzano)''')

    emailMessageHtml = (f'''
<html lang="en">
    <head></head>
    <body>
        <p>Hello,</p>
        <p>Update: {nowFormatted}</p>
        <br>
        <h2>World Data from <a href="https://www.worldometers.info/coronavirus/" target="_blank">WorldOMeter</a>:</h2>
        <table border="0" cellpadding="4px" cellspacing="0" height="auto" width="auto%">
            <tr>
                <td align="center" valign="top">Info</td>
                <td align="center" valign="top">Today's Data</td>
                <td align="center" valign="top">Yesterday's Data</td>
            </tr>
            <tr>
                <td align="left" valign"top">Cases since outbreak</td>
                <td align="left" valign"top">{worldCases}</td>
                <td align="left" valign"top">{maths(worldCases,wDifferenceCases)}</td>
            </tr>
            <tr>
                <td align="left" valign"top">Current Cases</td>
                <td align="left" valign"top">{currentWorldCases}</td>
                <td align="left" valign"top">{pastWorldCases}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Cases</td>
                <td align="left" valign"top">{wDifferenceCases}</td>
                <td align="left" valign"top">{wDifferenceCases1}</td>
            </tr>
            <tr>
                <td align="left" valign"top">Closed Cases</td>
                <td align="left" valign"top">{currentWorldClosed}</td>
                <td align="left" valign"top">{maths(currentWorldClosed,wDifferenceDeath,wDifferenceRecoveries)}</td>
            </tr>
            <tr>
                <td align="left" valign"top">Total Deaths</td>
                <td align="left" valign"top">{worldDeaths}</td>
                <td align="left" valign"top">{maths(worldDeaths,wDifferenceDeath)}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Deaths</td>
                <td align="left" valign"top">{wDifferenceDeath}</td>
                <td align="left" valign"top">{wDifferenceDeath1}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Deaths</td>
                <td align="left" valign"top">{wDifferenceDeath}</td>
                <td align="left" valign"top">{wDifferenceDeath1}</td>
            </tr>
            <tr>
                <td align="left" valign"top">Total Recoveries</td>
                <td align="left" valign"top">{worldRecoveries}</td>
                <td align="left" valign"top">{maths(worldRecoveries,wDifferenceRecoveries)}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Recoveries</td>
                <td align="left" valign"top">{wDifferenceRecoveries}</td>
                <td align="left" valign"top">{wDifferenceRecoveries1}</td>
            </tr>
        </table>
        <br>
        <h2>United States Data from <a href="https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html" target="_blank">CDC</a>:</h2>
        <table border="0" cellpadding="4px" cellspacing="0" height="auto" width="auto%">
            <tr>
                <td align="center" valign="top">Info</td>
                <td align="center" valign="top">Today's Data</td>
                <td align="center" valign="top">Yesterday's Data</td>
            </tr>
            <tr>
                <td align="left" valign"top">Total Cases</td>
                <td align="left" valign"top">{totals[0].text}</td>
                <td align="left" valign"top">{pastUsCases}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Cases</td>
                <td align="left" valign"top">{newCases}</td>
                <td align="left" valign"top">{pastUsNewCases}</td>
            </tr>
            <tr>
                <td align="left" valign"top">Total Deaths</td>
                <td align="left" valign"top">{totals[1].text}</td>
                <td align="left" valign"top">{pastUsDeaths}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Deaths</td>
                <td align="left" valign"top">{newDeaths}</td>
                <td align="left" valign"top">{pastUsNewDeaths}</td>
            </tr>
        </table>
        <br>
        <h2>California Data from <a href="https://www.sfchronicle.com/bayarea/article/Coronavirus-live-updates-news-bay-area-15237940.php" target="_blank">SF Chronicle</a>:</h2>
        <table border="0" cellpadding="4px" cellspacing="0" height="auto" width="auto%">
            <tr>
                <td align="center" valign="top">Info</td>
                <td align="center" valign="top">Today's Data</td>
                <td align="center" valign="top">Yesterday's Data</td>
            </tr>
            <tr>
                <td align="left" valign"top">Total Cases</td>
                <td align="left" valign"top">{californiaCases}</td>
                <td align="left" valign"top">{maths(californiaCases,calDifferenceCases)}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Cases</td>
                <td align="left" valign"top">{calDifferenceCases}</td>
                <td align="left" valign"top">{calDifferenceCases1}</td>
            </tr>
            <tr>
                <td align="left" valign"top">Total Deaths</td>
                <td align="left" valign"top">{californiaDeaths}</td>
                <td align="left" valign"top">{maths(californiaDeaths,calDifferenceDeaths)}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Deaths</td>
                <td align="left" valign"top">{calDifferenceDeaths}</td>
                <td align="left" valign"top">{calDifferenceDeaths1}</td>
            </tr>
        </table>
        <br>
        <h2>Bay Area from <a href="https://www.sfchronicle.com/bayarea/article/Coronavirus-live-updates-news-bay-area-15237940.php" target="_blank">SF Chronicle</a>:</h2>
        <table border="0" cellpadding="4px" cellspacing="0" height="auto" width="auto%">
            <tr>
                <td align="center" valign="top">Info</td>
                <td align="center" valign="top">Today's Data</td>
                <td align="center" valign="top">Yesterday's Data</td>
            </tr>
            <tr>
                <td align="left" valign"top">Total Cases</td>
                <td align="left" valign"top">{bayAreaCases}</td>
                <td align="left" valign"top">{maths(bayAreaCases,baDifferenceCases)}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Cases</td>
                <td align="left" valign"top">{baDifferenceCases}</td>
                <td align="left" valign"top">{baDifferenceCases1}</td>
            </tr>
            <tr>
                <td align="left" valign"top">Total Deaths</td>
                <td align="left" valign"top">{bayAreaDeaths}</td>
                <td align="left" valign"top">{maths(bayAreaDeaths,baDifferencesDeaths)}</td>
            </tr>
            <tr>
                <td align="left" valign"top">New Deaths</td>
                <td align="left" valign"top">{baDifferencesDeaths}</td>
                <td align="left" valign"top">{baDifferencesDeaths1}</td>
            </tr>
        </table>
        <br>
        <h4>- COVID-19 Reporter</h4>
        <p>(Created by <a href="https://rafaelcenzano.com" target="_blank">Rafael Cenzano</a>)</p>
    </body>
</html>''')

    for recieverEmail in recieverEmails:

        msg = MIMEMultipart('alternative')
        msg['From'] = f'COVID-19 Reporter <{senderEmail}>'
        msg['To'] = recieverEmail
        msg['Subject'] = f'CoronaVirus update: {nowFormatted}'
        part1 = MIMEText(emailMessage, 'plain')
        part2 = MIMEText(emailMessageHtml, 'html')
        msg.attach(part1)
        msg.attach(part2)
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
