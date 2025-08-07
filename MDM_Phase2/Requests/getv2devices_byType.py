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
log_file = os.path.join(log_dir, f"{timestamp}_getv2_devices_bytype.txt")
logger = setup_log(log_file, logger_name="file4")
#logger = setup_log(os.path.join(log_dir, f"{timestamp}_get_aggregate_view.text"))

def devices_bytype():

    print("Test initiated for get devices byType")
    logger.info("Test initiated for get devices byType")

    # importing the payload and config file:
    try:

        with open(config_file_path, "r") as f:
            config = json.load(f)
        url = config['url']
        token = config['token']
        logger.info("Imported the config file")

        with open(payload_import, "r") as f:
            data = json.load(f)

    except Exception as e:
        logger.error(f"Failed to import the json files: {e}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in config['models_v2']:

            #getting the device name from the config
            device = config['imported_devices'][m]

            #generate random reference id
            ref_id = str(random.randint(1000,9999))

            #modifying url
            model_url = f"{url}v2/catalog/deviceTypes/{m}?referenceId={ref_id}"

            response = requests.get(url=model_url, headers=headers, verify=False)
            rcode = response.status_code
            rbody = response.text

            print("Response code: ",rcode)
            print("Response Body: ",rbody)

            if rcode ==200:
                logger.info("Successfully received the response ")
                logger.info(f"Response code: {rcode}\nResponse Body: {rbody}")

                #check if the imported device is present here or not
                if device in rbody:
                    logger.info(f"Device {device} present in the response")
                    logger.info("="*20)
                else:
                    logger.error(f"Device {device} not present in the response")

            else:
                logger.error(f"Response code: {rcode}\nResponse Body: {rbody}")
    except Exception as e:
        print(f"Exception caused while request action: {e}")
        logger.error(f"Exception caused {e}")
    finally:
        logger.info("Test Completed")

#devices_bytype()