import requests

class WebServiceDevice:
    def __init__(self, url):
        self.url = url
    
    def getData(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            response = {}
        return response.json()