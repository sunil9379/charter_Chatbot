import copy
import random
import time

import deepdiff
from deepdiff import DeepDiff
import requests
import json
import urllib3
from dotenv import load_dotenv
import os
import datetime
from Requests.Log.logger_setup import setup_log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH")  # this is Requests directory path
payload_deploy = os.environ.get("PAYLOAD_DEPLOY")
payload_import = os.environ.get("PAYLOAD_IMPORT")


# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_excluded_devices.txt")
logger = setup_log(log_file, logger_name="file8")

def excluded_device():

    logger.info("Test initiated for get excluded deviceTypes V1")

    token = None
    url = None
    # Loading the config file
    try:

        with open(config_file_path,"r") as f:
            config = json.load(f)
            url = config.get("url")
            token = config.get("token")

    except Exception as e:
        logger.error(f"Exception occurred during loading config file {e}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Request Action
    try:

        url_v1 = f"{url}v1/fas/excludedDeviceTypes"

        response_v1 = requests.get(url=url_v1, headers=headers, verify=False)
        print(f"Response code: {response_v1.status_code}")
        print(f"Response text: {response_v1.json()}")

        if response_v1.status_code == 200:
            logger.info(f"Response code: {response_v1.status_code}")
            logger.info(f"Response : {response_v1.text}")
        else:
            logger.error(f"Response code: {response_v1.status_code}")
            logger.error(f"Response : {response_v1.text}")

    except Exception as e:
        logger.error("Error occurred ", e)
        print("Error occurred ", e)

    '''
    with open('Validation_json/excluded_device_types_v1.json', 'w') as f:
        f.write(json.dumps(response_v1.json(), indent=4))
    '''

    try:

        with open('Validation_json/excluded_device_types_v1.json', 'r') as f:
            v1_validation=json.load(f)

    except Exception as e:

        print("Error in opening v1 validation json", e)
        logger.error(f"Error in opening v1 validation json {e}")

    #Perform V1 validation by comparing the response json from requests and response already present
    v1_diff=DeepDiff(v1_validation, response_v1.json())
    if v1_diff !={}:

        logger.error(f"Error occurred {v1_diff}")
        print("Difference in V1 validation: ",v1_validation)

    else:
        print("V1 Validated")
        logger.info("V1 validated")


    logger.info("Test Completed for V1 deviceType")

    '''
    FOR V2 DEVICE TYPES
    '''

    print("V2 Execution")
    logger.info("Test initiated for get excluded deviceTypes V2")


    #Request Action
    try:

        url_v2 = config["url"] + "v2/fas/excludedDeviceTypes"
        response_v2=requests.get(url=url_v2,headers=headers,verify=False)
        print(f"Response code: {response_v2.status_code}")
        print(f"Response text: {response_v2.json()}")

        if response_v2.status_code == 200:
            logger.info(f"Response code: {response_v2.status_code}")
            logger.info(f"Response : {response_v2.text}")
        else:
            logger.error(f"Response code: {response_v2.status_code}")
            logger.error(f"Response : {response_v2.text}")

    except Exception as e:
        logger.error("Error occurred ",e)
        print("Error occurred ",e)

    '''
    with open('Validation_json/excluded_device_types_v2.json','w') as f:
        f.write(json.dumps(response_v2.json(),indent=4))
    '''

    try:

        with open('Validation_json/excluded_device_types_v2.json','r') as f:
            v2_validation = json.load(f)

    except Exception as e:

        print("Error in opening v2 validation json", e)
        logger.error(f"Error in opening v2 validation json {e}")


    #Perform V1 validation by comparing the response json from requests and response already present
    v2_diff = DeepDiff(v2_validation, response_v2.json())

    if v2_diff != {}:

        logger.error(f"Error occurred {v2_diff}")
        print("Difference in V2 validation: ", v2_validation)

    else:
        print("V2 Validated")
        logger.info("V2 validated")

    logger.info("Test Completed for V2 deviceType")

excluded_device()