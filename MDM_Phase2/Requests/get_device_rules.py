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
log_file = os.path.join(log_dir, f"{timestamp}_device_rules.txt")
logger = setup_log(log_file, logger_name="file7")

def device_rules():

    print("Test initiated for get device rules")
    logger.info("Test initiated for get device rules")


    # Loading the config file
    try:

        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]


    except Exception as e:
        logger.error("Exception occurred during loading config file", e)

    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    #initiate the request action
    try:

        if 'models_v2' in config:

            for m in config['models_v2']:

                ref_id = str(random.randint(1000,9999))

                device_url = url + "v2/catalog/deviceTypes/" + m + "/rules?referenceId=" + ref_id
                print("device url: ",device_url)
                print("Initiating request for get device rules")

                response = requests.get(url=device_url, headers=headers,verify=False)
                print("Response status code: ", response.status_code)
                print("Response text: ", response.text)

                if response.status_code == 200:
                    logger.info(f"Response status code: {response.status_code}")
                    logger.info(f"Response text: {response.text}")

                    #with open('Response_json/device_rules.json', 'w') as f:
                    #    json.dump(response.json(), f)

                else:
                    logger.error(f"Response status code: {response.status_code}")
                    logger.error(f"Response text: {response.text}")

        else:
            print("Models v2 not present in config.json")
            logger.error("Models v2 not present in config.json")

    except Exception as e:
        print("Exception for get device rules: ",e)
        logger.error(f"Exception for get device rules: {e}")

    finally:
        logger.info("Execution for get device rules completed")
        print("Execution Complete for get device rules completed")

#device_rules()