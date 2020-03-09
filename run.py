import requests
from bs4 import BeautifulSoup as bs
from time import sleep as delay
from secret import *
from smtplib import SMTP
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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

        nowFormatted = datetime.now().strftime('%-m/%-d/%y %-I:%-M %p')

        email_message = (f'''
Hello,

Update: {nowFormatted}

CDC updated @ {pageDate}

{cases}
{deaths}
{statesWith}

- Covid-19 reporter
                          ''')

        msg = MIMEMultipart()
        msg['From'] = f'covid-19 updater <{senderEmail}>'
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