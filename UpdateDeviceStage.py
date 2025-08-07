# Importing the required libraries
import requests
import json
import logging
from datetime import datetime
from logsetup import *
from dummydummy import *

# update model PUT method to update the stage of a device
def update_model_stage(url, payload, headers):
    logging.info("Starting the PUT method")
    response = requests.put(url, json=payload, headers=headers, verify=False)
    logging.info("executed the PUT method to update the model")
# Check and validating if the required response is rendered and logging the same in log file
    if response.status_code == 201:
        logging.info(f'response code:{response.status_code}')
        response_msg = str((json.loads(response.text))["detail"])
        if "updated device" in response_msg:
            print("Test Case is passed")
            print("Success!")
            logging.info("Test case passed")
            logging.info(f'response message: {response.json()}')
            print(response.json())  # or response.text for raw output


    else:
        logging.info("Test case failed")
        logging.info(response.text)
        logging.info(response.status_code)