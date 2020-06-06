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

    californiaParts = pTags[3].text[2:].split()
    californiaCases = californiaParts[0]
    californiaDeaths = californiaParts[len(californiaParts)-2]

    bayAreaParts = pTags[4].text[2:].split()
    bayAreaCases = bayAreaParts[0]
    bayAreaDeaths = bayAreaParts[len(bayAreaParts)-2]

    with open(jsonFilePath, 'r') as jsonFile:
        jsonDataRead = json.load(jsonFile)

    try:
        calCasesToday = int(''.join(californiaCases.split(',')))
    except:
        calCasesToday = jsonDataRead['calCasesToday']

    try:
        calDeathsToday = int(''.join(californiaDeaths.split(',')))
    except:
        calDeathsToday = jsonDataRead['calDeathsToday']

    try:
        baCasesToday = int(''.join(bayAreaCases.split(',')))
    except:
        baCasesToday = jsonDataRead['baCasesToday']
        bayAreaCases = jsonDataRead['baCasesToday']

    try:
        baDeathsToday = int(''.join(bayAreaDeaths.split(',')))
    except:
        baDeathsToday = jsonDataRead['baDeathsToday']
        bayAreaDeaths = jsonDataRead['baDeathsToday']

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

        jsonData = {'past':{'calCasesToday':calCasesToday, 'calDeathsToday':calDeathsToday, 'baCasesToday':baCasesToday, 'baDeathsToday':baDeathsToday, 'worldCases':worldCasesToday, 'worldDeaths':worldDeathsToday, 'worldRecoveries':worldRecoveriesToday},'past2':{'calCasesToday':calCasesToday, 'calDeathsToday':calDeathsToday, 'baCasesToday':baCasesToday, 'baDeathsToday':baDeathsToday, 'worldCases':worldCasesToday, 'worldDeaths':worldDeathsToday, 'worldRecoveries':worldRecoveriesToday}}

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

        calDifferenceCases = '{:,}'.format(calCasesToday - jsonDataFile['past']['calCasesToday'])
        calDifferenceDeaths = '{:,}'.format(calDeathsToday - jsonDataFile['past']['calDeathsToday'])
        baDifferenceCases = '{:,}'.format(baCasesToday - jsonDataFile['past']['baCasesToday'])
        baDifferencesDeaths = '{:,}'.format(baDeathsToday - jsonDataFile['past']['baDeathsToday'])
        wDifferenceCases = '{:,}'.format(worldCasesToday - int(jsonDataFile['past']['worldCases']))
        wDifferenceDeath = '{:,}'.format(worldDeathsToday - int(jsonDataFile['past']['worldDeaths']))
        wDifferenceRecoveries = '{:,}'.format(worldRecoveriesToday - int(jsonDataFile['past']['worldRecoveries']))

        calDifferenceCases1 = '{:,}'.format(jsonDataFile['past']['calCasesToday'] - jsonDataFile['past2']['calCasesToday'])
        calDifferenceDeaths1 = '{:,}'.format(jsonDataFile['past']['calDeathsToday'] - jsonDataFile['past2']['calDeathsToday'])
        baDifferenceCases1 = '{:,}'.format(jsonDataFile['past']['baCasesToday'] - jsonDataFile['past2']['baCasesToday'])
        baDifferencesDeaths1 = '{:,}'.format(jsonDataFile['past']['baDeathsToday'] - jsonDataFile['past2']['baDeathsToday'])
        wDifferenceCases1 = '{:,}'.format(jsonDataFile['past']['worldCasesToday'] - int(jsonDataFile['past2']['worldCases']))
        wDifferenceDeath1 = '{:,}'.format(jsonDataFile['past']['worldDeathsToday'] - int(jsonDataFile['past2']['worldDeaths']))
        wDifferenceRecoveries1 = '{:,}'.format(jsonDataFile['past']['worldRecoveriesToday'] - int(jsonDataFile['past2']['worldRecoveries']))

        jsonDataFile['past2'] = jsonDataFile['past']

        jsonDataFile['past']['calCasesToday'] = calCasesToday
        jsonDataFile['past']['calDeathsToday'] = calDeathsToday
        jsonDataFile['past']['baCasesToday'] = baCasesToday
        jsonDataFile['past']['baDeathsToday'] = baDeathsToday
        jsonDataFile['past']['worldCases'] = worldCasesToday
        jsonDataFile['past']['worldDeaths'] = worldDeathsToday
        jsonDataFile['past']['worldRecoveries'] = worldRecoveriesToday

        with open(jsonFilePath, 'w') as jsonFile:
            json.dump(jsonDataFile, jsonFile)

    emailMessage = (f'''
Hello,

Update: {nowFormatted}


World Data from WorldOMeter:

Total cases since outbreak: {worldCases}, Yesterday: {maths(worldCases,wDifferenceCases)}
Total current cases: {currentWorldCases}
New cases: {wDifferenceCases}, Yesterday: {wDifferenceCases1}

Total closed cases: {currentWorldClosed}, Yesterday: {maths(currentWorldClosed,wDifferenceDeath,wDifferenceRecoveries)}
Total deaths: {worldDeaths}, Yesterday: {maths(worldDeaths,wDifferenceDeath)}
New deaths: {wDifferenceDeath}, Yesterday: {wDifferenceDeath1}
Total Recoveries: {worldRecoveries}, Yesterday: {maths(worldRecoveries,wDifferenceRecoveries)}
New Recoveries: {wDifferenceRecoveries}, Yesterday: {wDifferenceRecoveries1}


United States Data from CDC:

Total cases: {totals[0].text}
New cases: {newCases}

Total deaths: {totals[1].text}
New deaths: {newDeaths}


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
<html>
    <head></head>
    <body>
        <p>Hello,</p>
        <p>Update: {nowFormatted}</p>
        <br>
        <h2>World Data from <a href="https://www.worldometers.info/coronavirus/" target="_blank">WorldOMeter</a>:</h2>
        <p>Total cases since outbreak: {worldCases}, Yesterday: {maths(worldCases,wDifferenceCases)}</p>
        <p>Total current cases: {currentWorldCases}</p>
        <p>New cases: {wDifferenceCases}, Yesterday: {wDifferenceCases1}</p>
        <p>Total closed cases: {currentWorldClosed}, Yesterday: {maths(currentWorldClosed,wDifferenceDeath,wDifferenceRecoveries)}</p>
        <p>Total deaths: {worldDeaths}, Yesterday: {maths(worldDeaths,wDifferenceDeath)}</p>
        <p>New deaths: {wDifferenceDeath}, Yesterday: {wDifferenceDeath1}</p>
        <p>Total Recoveries: {worldRecoveries}, Yesterday: {maths(worldRecoveries,wDifferenceRecoveries)}</p>
        <p>New Recoveries: {wDifferenceRecoveries}, Yesterday: {wDifferenceRecoveries1}</p>
        <br>
        <h2>United States Data from <a href="https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html" target="_blank">CDC</a>:</h2>
        <p>Total cases: {totals[0].text}</p>
        <p>New cases: {newCases}</p>
        <p>Total deaths: {totals[1].text}</p>
        <p>New deaths: {newDeaths}</p>
        <br>
        <h2>California Data from <a href="https://www.sfchronicle.com/bayarea/article/Coronavirus-live-updates-news-bay-area-15237940.php" target="_blank">SF Chronicle</a>:</h2>
        <p>Total cases: {californiaCases}, Yesterday: {maths(californiaCases,calDifferenceCases)}</p>
        <p>New cases: {calDifferenceCases}, Yesterday: {calDifferenceCases1}</p>
        <p>Total deaths: {californiaDeaths}, Yesterday: {maths(californiaDeaths,calDifferenceDeaths)}</p>
        <p>New deaths: {calDifferenceDeaths}, Yesterday: {calDifferenceDeaths1}</p>
        <br>
        <h2>Bay Area from <a href="https://www.sfchronicle.com/bayarea/article/Coronavirus-live-updates-news-bay-area-15237940.php" target="_blank">SF Chronicle</a>:</h2>
        <p>Total cases: {bayAreaCases}, Yesterday: {maths(bayAreaCases,baDifferenceCases)}</p>
        <p>New cases: {baDifferenceCases}, Yesterday: {baDifferenceCases1}</p>
        <p>Total deaths: {bayAreaDeaths}, Yesterday: {maths(bayAreaDeaths,baDifferencesDeaths)}</p>
        <p>New deaths: {baDifferencesDeaths}, Yesterday: {baDifferencesDeaths1}</p>
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