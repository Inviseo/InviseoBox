import os
import re
import sys
from Logger import Logger
# print(os.system('ls /dev'))
# print('url',os.getenv('url'))
# print('email',os.getenv('email'))
# print('password',os.getenv('password'))
# print('worker_id',os.getenv('worker_id'))
# print('interval',os.getenv('interval'))
logger = Logger()

def check_input_data():
    worker_id = os.getenv('worker_id')
    if worker_id is None:
        raise Exception("L'identifiant du worker n'est pas défini.")
    interval = os.getenv('interval')
    if interval is None:
        raise Exception("L'intervalle n'est pas défini.")
    # Check that worker_id is a valid ObjectId
    if (re.match(r'^[0-9a-fA-F]{24}$', worker_id) is None):
        raise Exception("L'identifiant du worker doit être un ObjectId valide.")
    # Check that the interval is a positive integer
    if not interval.isdigit() or int(interval) <= 0:
        raise Exception("L'intervalle doit être un entier positif.")
try:
    check_input_data()
except Exception as e:
    logger.error(f"[main.py] - Une erreur s'est produite lors de l'initialisation: {e}")
    exit(1)

logger.info(f"[main.py] - Initialisation réussie.")