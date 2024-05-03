import requests
from Logger import Logger
import time

class API:
    def __init__(self, url, email, password, worker_id, logger=Logger()):
        self.url = url
        self.email = email
        self.password = password
        self.worker_id = worker_id
        self.logger = logger
        self.token = None

    def get_token(self, number_of_attempts=0):
        while number_of_attempts < 3:
            try:
                number_of_attempts += 1
                payload = {"email": self.email, "password": self.password}
                response = requests.post(f"{self.url}/auth/login", json=payload)
                response.raise_for_status()
                data = response.json()
                try:
                    self.token = data["token"]
                except KeyError as e:
                    self.logger.log_error(f"[API.py] Pas de token - {e}")
            except requests.exceptions.HTTPError as e:
                self.logger.log_error(f"[API.py] - Une erreur s'est produite lors de la récupération du token: {e}")
            except requests.exceptions.Timeout:
                self.logger.log_error("[API.py] - Timeout lors de la récupération du token")
                time.sleep(5)
                self.get_token(number_of_attempts)
            except requests.exceptions.TooManyRedirects:
                self.logger.log_error("[API.py] - Trop de redirections lors de la récupération du token (URL incorrecte)")
            except requests.exceptions.RequestException as e:
                self.logger.log_error(f"[API.py] - Une erreur s'est produite lors de la récupération du token: {e}")
                time.sleep(5)
                self.get_token(number_of_attempts)

    def get_devices(self, number_of_attempts=0):
        while self.token is not None and number_of_attempts < 3:
            try:
                number_of_attempts += 1
                headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}
                devices = requests.get(f"{self.url}/workers/devices?id={self.worker_id}", headers=headers)
                devices.raise_for_status()
                return devices.json()
            except requests.exceptions.HTTPError as e:
                self.logger.log_error(f"[API.py] - Une erreur s'est produite lors de la récupération des appareils: {e}")
            except requests.exceptions.Timeout:
                self.logger.log_error("[API.py] - Timeout lors de la récupération des appareils")
                time.sleep(5)
                self.get_devices(number_of_attempts)
            except requests.exceptions.TooManyRedirects:
                self.logger.log_error("[API.py] - Trop de redirections lors de la récupération des appareils (URL incorrecte)")
            except requests.exceptions.RequestException as e:
                self.logger.log_error(f"[API.py] - Une erreur s'est produite lors de la récupération des appareils: {e}")

    def send_devices_status(self, status):
        try:
            headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}
            response = requests.post(f"{self.url}/devices/status", headers=headers, json=status)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.log_error(f"[API.py] - Une erreur s'est produite lors de l'enregistrement du statut des appareils: {e}")
        except requests.exceptions.Timeout:
            self.logger.log_error("[API.py] - Timeout lors de l'enregistrement du statut des appareils")
        except requests.exceptions.TooManyRedirects:
            self.logger.log_error("[API.py] - Trop de redirections lors de l'enregistrement du statut des appareils (URL incorrecte)")
        except requests.exceptions.RequestException as e:
            self.logger.log_error(f"[API.py] - Une erreur s'est produite lors de l'enregistrement du statut des appareils: {e}")

    def send_fields(self, fields):
        try:
            headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}
            response = requests.post(f"{self.url}/fields/bulk", headers=headers, json=fields)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.log_error(f"[API.py] - Une erreur s'est produite lors de l'envoi des données: {e}")
        except requests.exceptions.Timeout:
            self.logger.log_error("[API.py] - Timeout lors de l'envoi des données")
        except requests.exceptions.TooManyRedirects:
            self.logger.log_error("[API.py] - Trop de redirections lors de l'envoi des données (URL incorrecte)")
        except requests.exceptions.RequestException as e:
            self.logger.log_error(f"[API.py] - Une erreur s'est produite lors de l'envoi des données: {e}")