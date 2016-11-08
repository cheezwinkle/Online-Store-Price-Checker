#! python3
# rtpricecheck.py - Checks the current price of a product on the RoosterTeeth store.

import requests, bs4, datetime, smtplib, logging, configparser
from email.mime.text import MIMEText 

logging.basicConfig(filename='rtpricechecklog.txt', level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s - %(message)s')
config = configparser.ConfigParser()
config.read('config.ini')

def send_email(currPrice):
        logging.debug('Begin sending email')
        # Set email variables from config.ini
        emailsettings = config['Email Settings']
        smtp_server = emailsettings['smtp_server']
        smtp_port = emailsettings['smtp_port']
        smtp_login = emailsettings['login']
        smtp_pw = emailsettings['password']
        sender = emailsettings['sender']
        recipients = emailsettings['recipients'].split(',')
        
        msg = MIMEText('A price change was detected!\nNew price: $' + str(currPrice) + '\n' + config['Webpage Settings']['url'])
        msg['Subject'] = "RT Store Price Check Alert"
        msg['From']    = sender
        msg['To']      = ", ".join(recipients)
        
        s = smtplib.SMTP(smtp_server, int(smtp_port))
        s.ehlo()
        s.starttls()
        s.ehlo()
        logging.debug(msg.as_string())
        try:
                s.login(smtp_login, smtp_pw)
        except Exception as exc:
                logging.debug('There was an error: %s' % (exc))
        try:
                s.sendmail(msg['From'], recipients, msg.as_string())
        except Exception as exc:
                logging.debug('There was an error: %s' % (exc))
        else:
                logging.debug('Email sent')
        finally:
                s.quit()
                
# Begin script
logging.debug('Starting rtpricecheck')
webpagesettings = config['Webpage Settings']
standardPrice = float(webpagesettings['standard_price'])
currentPrice = 0.0

# Download the webpage
logging.debug('Downloading webpage')
url = webpagesettings['url']
res = requests.get(url)
try:
        res.raise_for_status()
except Exception as exc:
        logging.debug('There was an error: %s' % (exc))

# Parse HTML for price
logging.debug('Parsing HTML')
webPage = bs4.BeautifulSoup(res.text, 'html.parser')
elems = webPage.select('span[itemprop="price"]')

# Check number of prices found (should only be 1, but just in case)
if len(elems) > 1:
        logging.debug(len(elems), 'prices were found')
elif len(elems) == 1:
        logging.debug('1 price was found')
elif len(elems) < 1:
        logging.debug('No prices were found')

# Log prices       
for i in elems:
        logging.debug('The current price is %s',i.getText())
        
# Check if price has changed
if len(elems) == 1:
        currentPrice = float(elems[0].getText()[1:])
        if currentPrice < standardPrice:
                logging.debug('ALERT: Price has lowered!')
                send_email(currentPrice)
        elif currentPrice > standardPrice:
                logging.debug('ALERT: Price has increased!?')
                logging.debug('Not sending email.')
        else:
              logging.debug('No price change detected.')
              logging.debug('Not sending email.')