import json
import copy
import random
from dotenv import load_dotenv
import os
import datetime
from Phase_1.log_setup import setup_log
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("P1_CERTIFY_LOG_PATH")  # this is Requests directory path
payload_certify = os.environ.get("P1_CERTIFY_PAYLOAD")

# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_create_certify_devices.txt")
logger = setup_log(log_file, logger_name="file3")




def device_certify():
    logger.info("-------------------------------**----------------------------")
    print("Pushing the device from test to certify stage")
    logger.info("Pushing the device from test to certify stage")

    # importing the payload and config file:
    try:
        print("importing the payload file")

        with open(payload_certify, "r") as f:
            data = json.load(f)
            payload = copy.deepcopy(data)

        with open(config_file_path, "r") as f:
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
            #time.sleep(5)
            print(f"Payload for {m} device: {data_model}")
            device_name = content['test_devices'][m]

            device_url = url + "v2/catalog/models/" + device_name + "?status=Certified"
            print("device url: ",device_url)
            logger.info(f"device url: {device_url}")
            logger.info(f"data model: {data_model}")

            response = requests.put(url=device_url, headers=headers, json=data_model, verify=False)
            print("Response code: ",response.status_code)
            print("Response body: ",response.text)

            logger.info("======================================================")

            if response.status_code == 201:
                logger.info(f"Device {device_name} successfully pushed to certify stage")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Response body: {response.text}")

            else:
                logger.error(f"Device {device_name} failed to push to certify stage")
                logger.error(f"Error code: {response.status_code}")
                logger.error(f"Error message: {response.text}")
    except Exception as e:
        print(f"Failed to perform request action: {e}")

