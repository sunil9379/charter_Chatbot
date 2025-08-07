# Importing the required libraries
import requests
import json
import logging
from datetime import datetime
from logsetup import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_model(url, payload, headers):
    logging.info("Starting the POST method")
    response = requests.post(url, json=payload, headers=headers, verify=False)
    logging.info("executed the Post method to create the model")

# Check and validating if the required response is rendered and logging the same in log file
    if response.status_code == 201:
        logging.info(f'response code:{response.status_code}')
        response_msg = str((json.loads(response.text))["detail"])
        if "created document with id" in response_msg:
            logging.info("Test case passed")
            logging.info(f'response message: {response.json()}')


    else:
        logging.info("Test case failed")
        logging.info(response.text)
        logging.info(response.status_code)
