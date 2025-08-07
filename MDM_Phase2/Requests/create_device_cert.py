import copy
import random
import time

import requests
import json
import urllib3
from dotenv import load_dotenv
import os
import datetime
from Log.logger_setup import setup_log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH")  # this is Requests directory path

# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
logger = setup_log(os.path.join(log_dir, f"{timestamp}_device_creation.text"))


def create_device_certify():
    print("Pushing the device from trst to certify stage")
    logger.info("Pushing the device from trst to certify stage")

    # importing the payload and config file:
    try:
        print("importing the payload file")

        with open("device_certify.json", "r") as f:
            data = json.load(f)
            payload = copy.deepcopy(data)

        with open("config.json", "r") as f:
            content = json.load(f)
            url = content['url']
            token = content['token']
        logger.info("Imported the payload and config file")

    except Exception as e:
        logger.error(f"Failed to import the json files: {e}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in content['models_v2']:

            data_model = payload[m]
            print(f"Payload for {m} device: {data_model}")
            device_name = data_model['modelName']
            print(f"Model Name: {device_name}")

    except Exception as e:
        print(f"Failed to import the json files: {e}")

create_device_certify()