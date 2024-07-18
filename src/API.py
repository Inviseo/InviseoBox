import requests
from Logger import Logger
import time

class API:
    def __init__(self, url, token, logger=Logger()):
        self.url = url
        self.token = token
        self.logger = logger

    def get_devices(self, number_of_attempts=0):
        while number_of_attempts < 3:
            try:
                number_of_attempts += 1
                params = {"token": self.token}
                devices = requests.get(f"{self.url}/workers/devices", params=params)
                devices.raise_for_status()
                return devices.json()
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération des appareils: {e}")
            except requests.exceptions.Timeout:
                self.logger.error("[API.py] - Timeout lors de la récupération des appareils")
                time.sleep(5)
                return self.get_devices(number_of_attempts)
            except requests.exceptions.TooManyRedirects:
                self.logger.error("[API.py] - Trop de redirections lors de la récupération des appareils (URL incorrecte)")
                break
            except requests.exceptions.ConnectionError as e:
                self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération des appareils: {e}")
                break
            except requests.exceptions.RequestException as e:
                self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération des appareils: {e}")
                break
            except Exception as e:
                self.logger.error(f"[API.py] - Une erreur inattendue s'est produite lors de la récupération des appareils: {e}")
                break

    def send_devices_status(self, status):
        try:
            payload = {"token": self.token, "status": status}
            response = requests.post(f"{self.url}/devices/status", json=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de l'enregistrement du statut des appareils: {e}")
        except requests.exceptions.Timeout:
            self.logger.error("[API.py] - Timeout lors de l'enregistrement du statut des appareils")
        except requests.exceptions.TooManyRedirects:
            self.logger.error("[API.py] - Trop de redirections lors de l'enregistrement du statut des appareils (URL incorrecte)")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération des appareils: {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de l'enregistrement du statut des appareils: {e}")
        except Exception as e:
            self.logger.error(f"[API.py] - Une erreur inattendue s'est produite lors de l'enregistrement du statut des appareils: {e}")
    
    def send_fields(self, fields):
        try:
            payload = {"token": self.token, "fields": fields}
            response = requests.post(f"{self.url}/fields/bulk", json=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de l'envoi des données: {e}")
        except requests.exceptions.Timeout:
            self.logger.error("[API.py] - Timeout lors de l'envoi des données")
        except requests.exceptions.TooManyRedirects:
            self.logger.error("[API.py] - Trop de redirections lors de l'envoi des données (URL incorrecte)")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de l'envoi des données: {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de l'envoi des données: {e}")
        except Exception as e:
            self.logger.error(f"[API.py] - Une erreur inattendue s'est produite lors de l'envoi des données: {e}")

    def get_interval(self):
        try:
            # pour débugger, je veux afficher l'url interrogée avec les paramètres
            self.logger.debug(f"[API.py] - URL interrogée: {self.url}/workers/interval?token={self.token}")
            params = {"token": self.token}
            interval = requests.get(f"{self.url}/workers/interval", params=params)
            interval.raise_for_status()
            return interval.json()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération des intervalles: {e}")
        except requests.exceptions.Timeout:
            self.logger.error("[API.py] - Timeout lors de la récupération des intervalles")
        except requests.exceptions.TooManyRedirects:
            self.logger.error("[API.py] - Trop de redirections lors de la récupération des intervalles (URL incorrecte)")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération des intervalles: {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération des intervalles: {e}")
        except Exception as e:
            self.logger.error(f"[API.py] - Une erreur inattendue s'est produite lors de la récupération des intervalles: {e}")