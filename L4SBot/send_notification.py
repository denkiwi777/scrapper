from re import sub
import smtplib, ssl
import datetime
from load_config import *
from os.path import dirname, abspath
import logger as logger

d = dirname((dirname(abspath(__file__))))

config = load_config(d + '/config.yml')
emptylist = []


def append_messagge(testo):
    emptylist.append(testo)
    logger.write(testo)

def send_notification():
    body = ""
    subject ='Eseguzione L4SBot ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
    port =465 # FOR SSL
    smtp_server = "smtp.gmail.com"
    sent_from = config['EMAIL_ADDRESS']
    to = [config['EMAIL_ADDRESS_SEND']]
    for i in emptylist:
        body +=(i+"\n")
    message = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
            server.login(sent_from,config['EMAIL_PASSWORD'])
            server.sendmail(sent_from,to,message.encode('utf-8'))

    except Exception as e:
        print(e)        

def empty_list():
    emptylist.clear()