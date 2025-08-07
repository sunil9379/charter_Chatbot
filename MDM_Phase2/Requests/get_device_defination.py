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

#set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_device_definition.txt")
logger = setup_log(log_file, logger_name="file6")

def device_definition():

    print("Test initiated for get device definition")
    logger.info("Test initiated for get device definition")

    # Loading the config file
    try:

        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]

    except Exception as e:
        logger.error("Exception occurred during loading config file", e)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    #initiate the request action
    try:



                device_url_v1 = url + "v1/catalog/deviceTypes"
                device_url_v2 = url + "v2/catalog/deviceTypes"
                #print("device url: ",device_url)
                print("Initiating request for get device rules")

                response_v1 = requests.get(url=device_url_v1, headers=headers,verify=False)
                response_v2 = requests.get(url=device_url_v2, headers=headers,verify=False)
                print(f"Response status code for V1: {response_v1.status_code}")
                print(f"Response text: {response_v1.text}")
                print(f"Response status code for V2: {response_v2.status_code}")
                print(f"Response text: {response_v2.text}")

                if response_v1.status_code == 200 and response_v2.status_code == 200:
                    logger.info(f"Response status code for V1: {response_v1.status_code}")
                    logger.info(f"Response text for V1: {response_v1.text}")
                    logger.info(f"Response status code for V2: {response_v2.status_code}")
                    logger.info(f"Response text for V2: {response_v2.text}")


                else:
                    logger.error(f"Error code for V1: {response_v1.status_code}\nError code for V2: {response_v2.status_code}")
                    logger.error(f"Response text V1: {response_v1.text}\nResponse text V2: {response_v2.text}")


    except Exception as e:
        print("Exception for get device rules: ",e)
        logger.error(f"Exception for get device rules: {e}")

    finally:
        logger.info("Execution for get device definition completed")
        print("Execution Complete for get device definition completed")

#device_definition()