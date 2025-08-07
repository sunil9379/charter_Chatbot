import requests
import json
import logging
from  logsetup import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Send the GET request
def delete_model(url, headers):
    logging.info("Starting to delete the model")
    response = requests.delete(url, headers=headers, verify=False)
    # Check the status code and print the response
    if response.status_code == 204:
        logging.info("Test case passed")
        logging.info(f'response code:{response.status_code}')
        logging.info("successfully deleted the model")

    else:
        logging.info(f'response code:{response.status_code}')
        logging.info(response.text)













