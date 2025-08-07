import copy
import random
import re
import time

import deepdiff
from bs4 import BeautifulSoup
from deepdiff import DeepDiff
import requests
import json
import urllib3
from dotenv import load_dotenv
import os
import datetime
from Requests.Log.logger_setup import setup_log
from Requests.get_aggreagte_view import payload_deploy
from Requests.get_firmwareinfo import get_firmware_info

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH")  # this is Requests directory path
import_payload = os.environ.get("PAYLOAD_IMPORT")

# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_delete_firmware.txt")
logger = setup_log(log_file, logger_name="file3")
#logger = setup_log(os.path.join(log_dir, f"{timestamp}_delete_firmware.text"))


def firmware_delete():

    print("Test to delete the firmware initiated")
    logger.info("Test to delete the firmware initiated")

    try:
        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]

        with open(import_payload,"r") as f:
            data = json.load(f)

    except Exception as e:
        logger.error("Could not load config.json")


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in config['models_v2']:

            model_name = config['imported_devices'][m]
            print(f"deleting the firmware for {m} device type with model name: {model_name}")
            logger.info(f"deleting the firmware for {m} device type with model name: {model_name}")

            #fetching the firmwareVersion to delete from deploy payload
            payload =data[m]
            firmware = payload.get('data')[0].get('firmwareDesc').get('firmwareVersions')[2].get('firmwareVersion')
            print("firmware: ",firmware)

            #generate reference id
            ref_id = str(random.randint(1000,9999))

            #modifying the url
            firmware_url = f"{url}v2/catalog/models/{model_name}/firmwares/{firmware}?referenceId={ref_id}&userId=P3289462"

            #initiating requests:
            response = requests.delete(url=firmware_url, headers=headers, verify=False)
            print("Response code: ", response.status_code)
            print("Response body: ", response.text)

            if response.status_code == 204:
                logger.info(f"Firmware {firmware} successfully deleted")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Response body: {response.text}")

                #intiating get firmware info
                get_result = get_firmware_info(model_name,firmware)
                if m in get_result and get_result[m]["Status Code"]==404:
                    print(f"Firmware {firmware} deletion validated successfully")
                    logger.info(f"Firmware {firmware} successfully deleted\nStatus code: {get_result[m]['Status Code']}\nResponse Body: {get_result[m]['Response Body']}")
                else:
                    print(f"Cannot validate firmware {firmware} deleted or not")
                    logger.error(f"Error during validation\nStatus code: {get_result[m]['Status Code']}\nResponse Body: {get_result[m]['Response Body']}")
    except Exception as e:
            print(f"Exception occurred during request action: {e}")
            logger.error(f"Exception occurred during request action: {e}")

    finally:
        print("Test completed for deleting the firmware")
        logger.info("Test completed for deleting the firmware")

#firmware_delete()