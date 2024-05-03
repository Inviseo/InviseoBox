import requests
from Logger import Logger

class WebServiceDevice:
    def __init__(self, url, logger=Logger()):
        self.url = url
        self.logger = logger
    
    def getData(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            self.logger.log_error(f"[WebServiceDevice.py] - Une erreur s'est produite lors de la récupération des données: {e}")
            return None
        except requests.exceptions.Timeout:
            self.logger.log_error("[WebServiceDevice.py] - Timeout lors de la récupération des données")
            return None
        except requests.exceptions.TooManyRedirects:
            self.logger.log_error("[WebServiceDevice.py] - Trop de redirections lors de la récupération des données (URL incorrecte)")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.log_error(f"[WebServiceDevice.py] - Une erreur s'est produite lors de la récupération des données: {e}")
            return None

        return response.json()