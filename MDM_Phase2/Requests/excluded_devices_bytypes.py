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

def excluded_devices():

    print("Test initiated for get excluded devices")
    logger.info("Test initiated for get excluded devices")

    try:
        with open(config_file_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Config file not found")
        logger.error(f"config file not found")

    url = config.get("url")
    token = config.get("token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        url_v1 = f"{url}v1/fas/excludedDeviceTypes"
        url_v2 = f"{url}v2/fas/excludedDeviceTypes"

        response_v1 = requests.get(url=url_v1, headers=headers, verify=False)
        print(f"Response code: {response_v1.status_code}\nResponse body: {response_v1.text}")

        if response_v1.status_code == 200:
            logger.info(f"Response code: {response_v1.status_code}")
            logger.info(f"Response body: {response_v1.text}")
        else:
            logger.error(f"Error code: {response_v1.status_code}\nError message: {response_v1.text}")

        response_v2 = requests.get(url=url_v2, headers=headers, verify=False)
        print(f"Response code: {response_v2.status_code}\nResponse body: {response_v2.text}")

        if response_v2.status_code == 200:
            logger.info(f"Response code: {response_v2.status_code}")
            logger.info(f"Response body: {response_v2.text}")
        else:
            logger.error(f"Error code: {response_v2.status_code}\nError message: {response_v2.text}")

    except Exception as e:
        logger.error(f"Exception caused during requests action: {e}")
        print(f"Exception caused during requests action: {e}")

#excluded_devices()