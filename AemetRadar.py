import datetime
import os
import requests

project_path = os.getcwd()
class Radar:
    last_radar_filename = ""

    def get_radar(self):
        radar_url = "http://www.aemet.es/imagenes_d/eltiempo/observacion/radar/%year%month%day%hour%minute_r8ba.gif"
        print (radar_url)
        now = datetime.datetime.utcnow()
        year = str(now.year)
        month = "0" + str(now.month) if now.month < 10 else str(now.month)
        day = "0" + str(now.day) if now.day < 10 else str(now.day)
        hour = "0" + str(now.hour) if now.hour < 10 else str(now.hour)
        rounded_minute = int(now.minute / 10)
        minute = "00" if rounded_minute < 10 else str(rounded_minute)

        print(radar_url.replace('%year', year).replace('%month', month).replace("%day", day).replace("%hour", hour).replace("%minute", minute))

        filename = project_path + "/tmp_files_radar/" + year + month + day + hour + minute +".gif"

        if not os.path.exists(filename):
            r = requests.get(
                radar_url.replace('%year', year).replace('%month', month).replace("%day", day).replace("%hour",
                                                                                                       hour).replace(
                    "%minute", minute))
            if r.status_code == "400":
                filename = self.last_radar_filename
            else:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                    f.close()
                    self.last_radar_filename = filename
        return filename