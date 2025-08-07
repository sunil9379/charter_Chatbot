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
log_file = os.path.join(log_dir, f"{timestamp}_models_for_vendors.txt")
logger = setup_log(log_file, logger_name="file12")

def get_models_vendor():

    print("Test initiated to get models from specific vendors")
    logger.info("Test initiated to get models from specific vendors")


    #Loading the config file
    try:

        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]

    except Exception as e:
        logger.error("Exception occurred during loading config file",e)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        if 'vendors' in config.keys():

            for m in config['vendors']:
                model_url = url + "v1/catalog/vendors/" + m + "/models"
                #print("model url: ",model_url)

                #perform request action based on vendors
                response = requests.get(model_url, headers=headers, verify=False)
                print("Response code: ",response.status_code)
                print("Response text: ",response.text)

                if response.status_code == 200:

                    logger.info(f"Response code for {m} vendor: {response.status_code}")
                    logger.info(f"Response text {m} vendor: {response.text}")

                else:

                    logger.error(f"Response code for {m} vendor: {response.status_code}")
                    logger.error(f"Response text {m} vendor: {response.text}")

        else:
            print("Vendors not found in config.json")
            logger.error("Vendors not found in config.json")

    except Exception as e:
        print("Exception occurred ",e)
        logger.error("Exception occurred in Request Action ",e)

    finally:
        print("Test Completed for get models for specific vendors")
        logger.info("Test completed for get models for specific vendors")



#get_models_vendor()