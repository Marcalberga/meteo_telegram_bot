import requests
import time
import os

from AemetRadar import Radar
from Prediction import Comarcal

bot_token = 'Insert your token here'
project_path = os.getcwd()

def chuck():
    chuck_response = requests.request("GET", 'https://api.chucknorris.io/jokes/random').json()
    return chuck_response['value']

baseUrl = 'https://api.telegram.org/bot' + bot_token + '/'

updates = requests.request("GET", baseUrl + "getUpdates").json()

lastUpdate = False

comarcal = Comarcal()

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
            radar_image = Radar.get_radar()
            body_resposta = {
                "chat_id": result['message']['chat']['id'],
            }

            resposta_response = requests.request("POST",
                baseUrl + "sendPhoto",
                data=body_resposta,
                files={"photo": open(radar_image, "rb")}
                ).json()
        else:
            body_resposta = {
                "chat_id": result['message']['chat']['id'],
                "text": word_map.get(text_rebut, comarcal.meteo_comarca(text_rebut)),
                "parse_mode": "markdown"
            }

            resposta_response = requests.request("POST",
                 baseUrl + "sendMessage",
                 data=body_resposta
                 ).json()
        lastUpdate = result['update_id'] + 1

    time.sleep(1)

