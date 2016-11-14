#! python3

import smtplib, logging, configparser
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read('config.ini')
emailsettings = config['Email Settings']

def sendemail(currPrice):
        logging.info('Begin sending email')
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
        logging.info(msg.as_string())
        try:
                s.login(smtp_login, smtp_pw)
        except Exception as exc:
                logging.error('There was an error: %s' % (exc))
        try:
                s.sendmail(msg['From'], recipients, msg.as_string())
        except Exception as exc:
                logging.error('There was an error: %s' % (exc))
        else:
                logging.info('Email sent')
        finally:
                s.quit()