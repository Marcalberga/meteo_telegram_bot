import requests
import time
import datetime
import os
import xml.etree.ElementTree as ET

bot_token = '685525589:AAFFvEeeBt2v4vV4hnfOZvk570LiaKDhylo'
project_path = os.getcwd()

def get_radar():
    radar_url = "http://www.aemet.es/imagenes_d/eltiempo/observacion/radar/%year%month%day%hour%minute_r8ba.gif"
    now = datetime.datetime.utcnow()
    year = str(now.year)
    month = "0" + str(now.month) if now.month < 10 else str(now.month)
    day = "0" + str(now.day) if now.day < 10 else str(now.day)
    hour = "0" + str(now.hour) if now.hour < 10 else str(now.hour)
    rounded_minute = int(now.minute / 10)
    minute = "00" if rounded_minute < 10 else str(rounded_minute)

    print(radar_url.replace('%year', year).replace('%month', month).replace("%day", day).replace("%hour", hour).replace("%minute", minute))

    r = requests.get(radar_url.replace('%year', year).replace('%month', month).replace("%day", day).replace("%hour", hour).replace("%minute", minute))

    with open(project_path + "/tmp_image.gif", 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
        f.close()

    return "tmp_image"

def chuck():
    chuck_response = requests.request("GET", 'https://api.chucknorris.io/jokes/random').json()
    return chuck_response['value']

def get_precipitacio(int):
    prec_map = {
        1: "no se n'espera",
        2: "No es descarta",
        3: "possible",
        4: "probable",
        5: "molt probable"
    }

    return prec_map.get(int)

def meteo_comarca(text, xml):
    #TODO: Solucionar "Pla d'urgell" "Pla de l'estany" "Pallars Jussà" per el replace "la"
    id_comarca = 0

    for child in xml:
        if child.get('nomcomarca') == text:
            id_comarca = child.get('id')

    string = False

    for comarca in xml.iter('prediccio'):
        elemt_id_comarca = comarca.attrib.get('idcomarca')
        if elemt_id_comarca == id_comarca:
            max = comarca[0].attrib.get('tempmax')
            min = comarca[0].attrib.get('tempmin')
            prec = (int(comarca[0].attrib.get('probprecipitaciomati')) + int(comarca[0].attrib.get('probprecipitaciotarda'))) / 2



            string = """Avui: 
Temperatura màxima: """ + str(max) + """, 
Temperatura mínima: """ + str(min) + """, 
Probabilitat precipitació: """ + str(get_precipitacio(prec))

            maxd = comarca[1].attrib.get('tempmax')
            mind = comarca[1].attrib.get('tempmin')
            precd = (int(comarca[1].attrib.get('probprecipitaciomati')) + int(
                comarca[1].attrib.get('probprecipitaciotarda'))) / 2

            string += """

Demà:
Temperatura màxima: """ + str(max) + """, 
Temperatura mínima: """ + str(min) + """, 
Probabilitat precipitació: """ + str(get_precipitacio(prec))

    if not string:
        string = "escriu 'help' per veure les comandes o comprova que has escrit bé la comarca"

    return string

baseUrl = 'https://api.telegram.org/bot' + bot_token + '/'

updates = requests.request("GET", baseUrl + "getUpdates").json()

variableToStopDebugger = True

lastUpdate = False

xml_meteo = requests.request("GET", "http://static-m.meteo.cat/content/opendata/ctermini_comarcal.xml").content

formatted_xml = xml_meteo.lower().decode().replace("l'", "").replace("el ", "").replace("la ", "")

root = ET.fromstring(formatted_xml)

while True:
    if not lastUpdate:
        updatesUrl = baseUrl + "getUpdates"
    else:
        updatesUrl = baseUrl + "getUpdates?offset=" + str(lastUpdate)
    updates = requests.request("GET", updatesUrl).json()
    for result in updates['result']:
        text_rebut = result['message']['text'].lower()
        print(text_rebut)

        word_map = {
            "/start": "escriu el nom de la comarca que vols la méteo o escriu 'radar' per veure la última imatge",
            "/chuck": chuck(),
            "burro": "No tant com tu!",
            "puta": "ta mare!",
            "ei": "Sigues més original...",
            "hola": "hola! sóc una merda de bot programat per un pallasso! Escriu Help per veure què pots fer",
            "help": "/chuck o el que vulguis",
            "/help": "escriu el nom de la comarca per veure la previsió, o escriu radar per veure lúltima imatge de radar"
        }

        if text_rebut == "radar":
            radar_image = get_radar()
            body_resposta = {
                "chat_id": result['message']['chat']['id'],
            }

            resposta_response = requests.request("POST",
                 baseUrl + "sendPhoto",
                 data=body_resposta,
                 files={"photo": open(project_path + "/" + radar_image + ".gif", "rb")}
                 ).json()
        else:
            body_resposta = {
                 "chat_id": result['message']['chat']['id'],
                 "text": word_map.get(text_rebut, meteo_comarca(text_rebut, root))
            }

            resposta_response = requests.request("POST",
                 baseUrl + "sendMessage",
                 data=body_resposta
                 ).json()
        lastUpdate = result['update_id'] + 1
        variableToStopDebugger2 = True

    time.sleep(1)

