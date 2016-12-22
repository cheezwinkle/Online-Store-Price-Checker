#! python3
#  pricecheck.py - Checks the current price of a product on an online store.

import requests, bs4, datetime, smtplib, logging, configparser, re
from sendemail import sendemail

logging.basicConfig(filename='pricecheckerlog.txt', level=logging.INFO, format=' %(asctime)s -  %(levelname)s - %(message)s')
config = configparser.ConfigParser()
config.read('config.ini')
               
# Begin script
logging.info('Starting pricecheck')
webpagesettings = config['Webpage Settings']
standardPrice   = float(webpagesettings['standard_price'].replace(',', '.'))
currentPrice    = 0.0

# Download the webpage
logging.info('Downloading webpage')
url = webpagesettings['url']
res = requests.get(url)
try:
        res.raise_for_status()
except Exception as exc:
        logging.error('There was an error: %s' % (exc))

# Parse HTML for price
logging.info('Parsing HTML')
htmlTags = webpagesettings['html_tags']
logging.debug(htmlTags)
webPage = bs4.BeautifulSoup(res.text, 'html.parser')
elems = webPage.select(htmlTags)

# Check number of prices found (should only be 1, but just in case)
if len(elems) > 1:
        logging.info('%i prices were found' % len(elems))
elif len(elems) == 1:
        logging.info('1 price was found')
elif len(elems) < 1:
        logging.info('No prices were found')

# Log prices       
for i in elems:
        logging.info('The current price is %s' % i.getText())
        
# Check if price has changed
if len(elems) == 1:
        try:
                cleanPrice = re.sub('[^0-9,.]+', '', elems[0].getText().replace(',', '.'))
                currentPrice = float(cleanPrice)
                if currentPrice < standardPrice:
                        logging.info('ALERT: Price has lowered!')
                        sendemail(currentPrice)
                elif currentPrice > standardPrice:
                        logging.info('ALERT: Price has increased!?')
                        logging.info('Not sending email.')
                else:
                        logging.info('No price change detected.')
                        logging.info('Not sending email.')
        except Exception as exc:
                logging.error('There was an error: %s' % (exc))