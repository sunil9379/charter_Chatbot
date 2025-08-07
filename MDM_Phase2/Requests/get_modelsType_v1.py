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
payload_import = os.environ.get("PAYLOAD_IMPORT") # this is Requests directory path

#set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_getv1_devices_bytype.txt")
logger = setup_log(log_file, logger_name="file5")
#logger = setup_log(os.path.join(log_dir, f"{timestamp}_get_aggregate_view.text"))

def devicev1_bytype():

    print("test initiated for get device types by models")
    logger.info("Test initiated for get device types by models ")

   # Loading the config file
    try:

        with open(config_file_path,"r") as f:
            config = json.load(f)
    except Exception as e:
        logger.error("Exception occurred during loading config file", e)

    url = config.get("url")
    token = config.get("token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        if 'models_v1' in config:

            for i in config['models_v1']:

                model_url=url+"v1/catalog/deviceTypes/"+i
                response_i=requests.get(url=model_url,headers=headers,verify=False)

                if response_i.status_code==200:

                    print(f"Response code for {i}: {response_i.status_code}")
                    print(f"Response for {i}: {response_i.json()}")

                    logger.info(f"Response code {i} model: {response_i.status_code}")
                    logger.info(f"Response text {i} model: {response_i.json()}")


                else:
                    print(f"Response code: {response_i.status_code}")
                    print(f"Response: {response_i.json()}")

                    logger.error(f"Response code for {i} model: {response_i.status_code}")
                    logger.error(f"Response text {i} model: {response_i.json()}")

        else:
            print("No models defined")
            logger.error("No models defined in config.json")

    except Exception as e:
        logger.error(e)
        print(e)

    finally:
        print("Test execution completed for get models type v1")
        logger.info("Test execution completed for get models type v1")

#devicev1_bytype()