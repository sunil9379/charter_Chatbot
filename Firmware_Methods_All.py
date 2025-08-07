import json
import time
from logsetup import *
import requests
from deepdiff import DeepDiff

def check_json_content(main_json, specific_json):
    diff = DeepDiff(main_json, specific_json, ignore_order=True)
    return 'dictionary_item_added' not in diff and 'values_changed' not in diff

def create_firmware(url, payload, headers):
    logging.info("Starting the POST method to create a firmware")
    response = requests.post(url, json=payload, headers=headers, verify=False)
    logging.info("executed the Post method to create the firmware")
    # Check and validating if the required response is rendered and logging the same in log file
    if response.status_code == 201:
        logging.info(f'response code:{response.status_code}')
        #response_msg = str((json.loads(response.json())))
        #if "updated firmware in document with id" in response_msg:
        logging.info("Test case passed")
        logging.info(f'response message: {response.json()}')


    else:
        logging.info("Test case failed")
        logging.info(response.text)
        logging.info(response.status_code)
def get_firmware_v2(url,headers,payload):
    logging.info("Starting the GET method to retrieve a firmware details")
    response = requests.get(url, headers=headers, verify=False)
    logging.info("executed the GET method to retrieve a firmware details")
    if response.status_code == 200:
        if str(json.loads(response.json()["firmwareVersion"])) == str(json.loads(payload["firmwareVersion"])) and str(json.loads(response.json()["firmwareFilename"])) == str(json.loads(payload["firmwareFilename"])):
            logging.info(f'response code:{response.status_code}')
            logging.info("Test case passed")
            logging.info(f'response message: {response.json()}')
        else:
            logging.info("Test case failed")
    else:
        logging.error(f'Failed with Status code: {response.status_code}')
        logging.error(response.text)




