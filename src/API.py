import requests
from Logger import Logger
import time

class API:
    def __init__(self, url, token, logger=Logger()):
        self.url = url
        self.token = token
        self.logger = logger

    def get_worker(self, number_of_attempts=0):
        while number_of_attempts < 3:
            try:
                number_of_attempts += 1
                params = {"token": self.token}
                worker = requests.get(f"{self.url}/workers", params=params)
                worker.raise_for_status()
                return worker.json()
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération du worker: {e}")
            except requests.exceptions.Timeout:
                self.logger.error("[API.py] - Timeout lors de la récupération du worker")
                time.sleep(5)
                return self.get_worker(number_of_attempts)
            except requests.exceptions.TooManyRedirects:
                self.logger.error("[API.py] - Trop de redirections lors de la récupération du worker (URL incorrecte)")
                break
            except requests.exceptions.ConnectionError as e:
                self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération du worker: {e}")
                break
            except requests.exceptions.RequestException as e:
                self.logger.error(f"[API.py] - Une erreur s'est produite lors de la récupération du worker: {e}")
                break
            except Exception as e:
                self.logger.error(f"[API.py] - Une erreur inattendue s'est produite lors de la récupération du worker: {e}")
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
