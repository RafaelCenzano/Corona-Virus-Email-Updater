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

    totals = soup.findAll(attrs={'class':'count'})
    newCasesData = soup.findAll(attrs={'class':'new-cases'})

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

    r3 = requests.get('https://www.worldometers.info/coronavirus/')
    page3 = r3.text
    soup3 = bs(page3, 'lxml')

    spanTags = soup3.findAll('span')
    totalsWorld = soup3.findAll('div', attrs={'class':'number-table-main'})

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

        jsonData = {'calCasesToday':calCasesToday, 'calDeathsToday':calDeathsToday, 'baCasesToday':baCasesToday, 'baDeathsToday':baDeathsToday, 'worldCases':worldCasesToday, 'worldDeaths':worldDeathsToday, 'worldRecoveries':worldRecoveriesToday}

        with open(jsonFilePath, 'w') as jsonFile:
            json.dump(jsonData, jsonFile)

        calDifferenceCases = 'Unknown'
        calDifferenceDeaths = 'Unknown'
        baDifferenceCases = 'Unknown'
        baDifferencesDeaths = 'Unknown'
        wDifferenceCases = 'Unknown'
        wDifferenceDeath = 'Unknown'
        wDifferenceRecoveries = 'Unknown'

    else:

        with open(jsonFilePath, 'r') as jsonFile:
            jsonData = json.load(jsonFile)

        calDifferenceCases = '{:,}'.format(calCasesToday - jsonData['calCasesToday'])
        calDifferenceDeaths = '{:,}'.format(calDeathsToday - jsonData['calDeathsToday'])
        baDifferenceCases = '{:,}'.format(baCasesToday - jsonData['baCasesToday'])
        baDifferencesDeaths = '{:,}'.format(baDeathsToday - jsonData['baDeathsToday'])
        wDifferenceCases = '{:,}'.format(worldCasesToday - int(jsonData['worldCases']))
        wDifferenceDeath = '{:,}'.format(worldDeathsToday - int(jsonData['worldDeaths']))
        wDifferenceRecoveries = '{:,}'.format(worldRecoveriesToday - int(jsonData['worldRecoveries']))

        jsonData['calCasesToday'] = calCasesToday
        jsonData['calDeathsToday'] = calDeathsToday
        jsonData['baCasesToday'] = baCasesToday
        jsonData['baDeathsToday'] = baDeathsToday
        jsonData['worldCases'] = worldCasesToday
        jsonData['worldDeaths'] = worldDeathsToday
        jsonData['worldRecoveries'] = worldRecoveriesToday

        with open(jsonFilePath, 'w') as jsonFile:
            json.dump(jsonData, jsonFile)

    emailMessage = (f'''
Hello,

Update: {nowFormatted}


World Data from WorldOMeter:

Total cases: {worldCases}
Total current cases: {currentWorldCases}
New cases: {wDifferenceCases}

Total closed cases: {currentWorldClosed}
Total deaths: {worldDeaths}
New deaths: {wDifferenceDeath}
Total Recoveries: {worldRecoveries}
New Recoveries: {wDifferenceRecoveries}


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


Bay Area from SF Chronicle:

Total cases: {bayAreaCases}
New cases: {baDifferenceCases}

Total deaths: {bayAreaDeaths}
New deaths: {baDifferencesDeaths}


- COVID-19 Reporter
(Created by Rafael Cenzano)''')

    emailMessageHtml = (f'''
<html>
    <head></head>
    <body>
        <p>Hello,</p>
        <p>Update: {nowFormatted}</p>
        <br>
        <h2>World Data from <a href="https://www.worldometers.info/coronavirus/" target="_blank">WorldOMeter</a>:</h2>
        <p>Total cases: {worldCases}</p>
        <p>Total current cases: {currentWorldCases}</p>
        <p>New cases: {wDifferenceCases}</p>
        <p>Total closed cases: {currentWorldClosed}</p>
        <p>Total deaths: {worldDeaths}</p>
        <p>New deaths: {wDifferenceDeath}</p>
        <p>Total Recoveries: {worldRecoveries}</p>
        <p>New Recoveries: {wDifferenceRecoveries}</p>
        <br>
        <h2>United States Data from <a href="https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html" target="_blank">CDC</a>:</h2>
        <p>Total cases: {totals[0].text}</p>
        <p>New cases: {newCases}</p>
        <p>Total deaths: {totals[1].text}</p>
        <p>New deaths: {newDeaths}</p>
        <br>
        <h2>California Data from <a href="https://www.sfchronicle.com/bayarea/article/Coronavirus-live-updates-news-bay-area-15237940.php" target="_blank">SF Chronicle</a>:</h2>
        <p>Total cases: {californiaCases}</p>
        <p>New cases: {calDifferenceCases}</p>
        <p>Total deaths: {californiaDeaths}</p>
        <p>New deaths: {calDifferenceDeaths}</p>
        <br>
        <h2>Bay Area from <a href="https://www.sfchronicle.com/bayarea/article/Coronavirus-live-updates-news-bay-area-15237940.php" target="_blank">SF Chronicle</a>:</h2>
        <p>Total cases: {bayAreaCases}</p>
        <p>New cases: {baDifferenceCases}</p>
        <p>Total deaths: {bayAreaDeaths}</p>
        <p>New deaths: {baDifferencesDeaths}</p>
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