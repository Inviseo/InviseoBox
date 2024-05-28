import requests
from Logger import Logger

class WebServiceDevice:
    def __init__(self, url, logger=Logger()):
        self.url = url
        self.logger = logger
    
    def getData(self):
        try:
            response = requests.get(self.url, timeout=25)
            response.raise_for_status()
            return True, response.json()

        except requests.exceptions.HTTPError as e:
            self.logger.error(f"[WebServiceDevice.py] - Une erreur s'est produite lors de la récupération des données: {e}")
        except requests.exceptions.Timeout:
            self.logger.error("[WebServiceDevice.py] - Timeout lors de la récupération des données")
        except requests.exceptions.TooManyRedirects:
            self.logger.error("[WebServiceDevice.py] - Trop de redirections lors de la récupération des données (URL incorrecte)")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"[WebServiceDevice.py] - Une erreur s'est produite lors de la récupération des données: {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[WebServiceDevice.py] - Une erreur s'est produite lors de la récupération des données: {e}")
        except Exception as e:
            self.logger.error(f"[WebServiceDevice.py] - Une erreur inattendue s'est produite lors de la récupération des données: {e}")

        return False, None