import datetime
from encodings import utf_8
import time
from store_listing import check_existing_listing
from load_config import *
from telegramNotifier import *
from store_listing import store_listing
import traceback
import logger as logger
import requests
from os.path import dirname, abspath

d = (dirname(abspath(__file__)))

config = load_config(d + '/configurazione.yml')
lingue = config['lingue']
frasi = dict(config['CHIAVI_RICERCA'])
key = "key=" + config['KEY_GOOGLE']


def main():

    try:
        totalReq = 0
       
        append_message("-------------" +
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                        "-------------")
        append_message("-------------Inizio eseguzione nuova-------------")
        sendNotification()
        empty_list()
        for lingua in lingue:    
            append_message("Lingua:" + lingua['name'])
            counter = 0
            for frase in frasi.get(lingua['lingua']):                
                append_message("Inizio la ricerca per la frase:" + frase + "( " +
                            frasi.get("IT")[counter] + ")")
                baseUrl = "https://customsearch.googleapis.com/customsearch/v1/siterestrict?"
                sendNotification()
                empty_list()
                cx = "cx=" + lingua['cx']
                q = ("exactTerms=" + (frase.replace(" ", "%20"))).encode()
                finalUrl = baseUrl + cx + "&" + q.decode(
                'utf_8') + "&sort=date" + "&" + key
                if (totalReq == 90):
                    append_message(
                    "Limite giornaliero di richieste raggiunto ,si prosegue domani!!!!")
                    sendNotification()
                    logger.write("Email inviata")
                    time.sleep(90000)
                    empty_list()

                request = requests.get(url=finalUrl)
                totalReq = totalReq + 1
                data = request.json()
                if 'items' not in data:
                    print(("Nessun Annuncio trovato per la frase " +  frasi.get("IT")[counter] +
                      " per la lingua " + lingua['lingua']))
                    append_message("-->Nessun Annuncio trovato per la frase " +
                                frase + " per la lingua " + lingua['lingua'])
                    counter = counter + 1 
                    sendNotification()
                    empty_list()               
                    continue
                for annuncio in data['items']:
                    testo = annuncio['title']
                    link = annuncio['link']
                    if "/tag/" not in link and "/tags/" not in link:
                        if check_existing_listing(link):
                            print("Articolo gia trovato procedo con la prossima frase")
                            break                           
                        else:
                            store_listing(link)
                            append_message("Trovato link nuovo per la frase " +
                                        frase + "( " +
                                        frasi.get("IT")[counter] + ")" +
                                        " per la lingua " + lingua['lingua'])
                            print("Trovato link nuovo per la frase " +
                              "( " + frasi.get("IT")[counter] + ")" +
                              " per la lingua " + lingua['lingua'])
                            append_message("Titolo: " + testo)
                            append_message("Link: " + link)
                            sendNotification()
                            empty_list()
                counter = counter + 1                
        
        logger.write("Email inviata")
    except Exception as e:
        print("Oops!", traceback.format_exc(), "occurred.")
        with open(d + "\\errori.txt", 'a') as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f") +
                    "\n")
            traceback.print_exc(file=f)


main()