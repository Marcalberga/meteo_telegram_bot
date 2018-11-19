import requests
import xml.etree.ElementTree as ET

class Comarcal:
    root = None

    emojis = {
        1: u'\U00002600',
        2: u'\U000026C5',
        3: u'\U000026C5',
        4: u'\U00002601',
        5: u'\U0001F4A7',
        6: u'\U00002614',
        7: u'\U00002614',
        8: u'\U0001F4A8',
        9: u'\U0001F4A8',
        10: u'\U00002744',
        11: u'\U00002601',
        12: u'\U0001F301',
        13: u'\U00002744',
        20: u'\U00002601',
        21: u'\U00002601',
        22: u'\U0001F4A7',
        23: u'\U00002614',
        24: u'\U0001F4A8',
        25: u'\U0001F4A8',
        26: u'\U00002614',
        27: u'\U00002744',
        28: u'\U000026C4',
        29: u'\U0001F4A8',
        30: u'\U00002744',
        31: u'\U00002614',
        32: u'\U0001F4A7',
    }

    def __init__(self):
        xml_meteo = requests.request("GET", "http://static-m.meteo.cat/content/opendata/ctermini_comarcal.xml").content

        formatted_xml = xml_meteo.lower().decode()

        self.root = ET.fromstring(formatted_xml)

    def get_precipitacio(self, value):
        prec_map = {
            1: "no se n'espera",
            2: "No es descarta",
            3: "possible",
            4: "probable",
            5: "molt probable"
        }

        return prec_map.get(value)

    def meteo_comarca(self, text):
        text.replace("/", "")
        # TODO: Solucionar "Pla d'urgell" "Pla de l'estany" "Pallars Jussà" per el replace "la"
        id_comarca = 0

        for child in self.root:
            nom_comarca = str(child.get('nomcomarca'))
            if text in nom_comarca:
                id_comarca = child.get('id')

        string = False

        for comarca in self.root.iter('prediccio'):
            elemt_id_comarca = comarca.attrib.get('idcomarca')
            if elemt_id_comarca == id_comarca:
                max = comarca[0].attrib.get('tempmax')
                min = comarca[0].attrib.get('tempmin')
                prec = (int(comarca[0].attrib.get('probprecipitaciomati')) + int(
                    comarca[0].attrib.get('probprecipitaciotarda'))) / 2

                simbol_mati = self.emojis.get(int(comarca[0].attrib.get("simbolmati").replace('.png', '')))
                simbol_tarda = self.emojis.get(int(comarca[0].attrib.get("simboltarda").replace('.png', '')))

                prec_string = self.get_precipitacio(int(prec))

                string = """*Avui:* Matí: """ + str(simbol_mati) + """ - Tarda: """ + str(simbol_tarda) + """
    Temperatura màxima: """ + str(max) + """, 
    Temperatura mínima: """ + str(min) + """, 
    Probabilitat precipitació: """ + prec_string

                maxd = comarca[1].attrib.get('tempmax')
                mind = comarca[1].attrib.get('tempmin')
                precd = (int(comarca[1].attrib.get('probprecipitaciomati')) + int(
                    comarca[1].attrib.get('probprecipitaciotarda'))) / 2

                simbol_matid = self.emojis.get(int(comarca[0].attrib.get("simbolmati").replace('.png', '')))
                simbol_tardad = self.emojis.get(int(comarca[0].attrib.get("simboltarda").replace('.png', '')))

                prec_stringd = self.get_precipitacio(int(precd))

                string += """

*Demà:* Matí: """ + str(simbol_mati) + """ - Tarda: """ + str(simbol_tarda) + """
    Temperatura màxima: """ + str(maxd) + """, 
    Temperatura mínima: """ + str(mind) + """, 
    Probabilitat precipitació: """ + prec_stringd

        if not string:
            string = "escriu 'help' per veure les comandes o comprova que has escrit bé la comarca"

        return string