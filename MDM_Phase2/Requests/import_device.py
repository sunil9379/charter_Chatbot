import copy
import random
import re
import time
from Requests.kafka_info import read_kafka
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH")  # this is Requests directory path
payload_import = os.environ.get("PAYLOAD_IMPORT")

# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_import_device.txt")
logger = setup_log(log_file, logger_name="file1")


def device_import():

    print("Test initiated for import device")
    logger.info("Test initiated for import device")

    try:
        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]

        with open(payload_import,"r") as f:
            data = json.load(f)

    except Exception as e:
        logger.error("Could not load config.json")


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in config['models_v2']:

            payload = data[m]

            #fetch the device name
            device_name = payload.get("data")[0].get("modelName")
            print(device_name)

            #fetch the required data for validation
            val_payload = payload.get("data")[0]
            import_url = url + "v2/catalog/deviceTypes/import"

            #'''
            response = requests.post(url=import_url, headers=headers, json=payload, verify=False)
            print(f"Rsponse code: {response.status_code}")
            print(f"Response body: {response.text}")

            if response.status_code == 201 or response.status_code == 500 or response.status_code == 503:
                logger.info(f"Successfully imported {device_name} device")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Response body: {response.text}")

                config['imported_devices'][m]=device_name
                with open(config_file_path,"w") as f:
                    json.dump(config,f,indent=4)

                #performing validation
                logger.info("Validating the response payload matches original payload")

                ref_id = str(random.randint(1000,9999))
                #model_url = f"{url}v2/catalog/models/{device_name}?referenceId={ref_id}"
                model_url = url + "v2/catalog/models/" + device_name + "?referenceId=" + ref_id
                print("get url: ",model_url)

                message,present = read_kafka("deviceopedia-authoritative-incremental-device-model-qa",device_name)
                print("Message from kafka: ",message)
                #print(f"type: {type(message)}")
                if present:
                    logger.info(f"kafka message published for model: {device_name}")
                else:
                    logger.error(f"message was not published in kafka for model: {device_name}")
                #topics = ["deviceopedia-authoritative-full-device-model-qa","deviceopedia-authoritative-incremental-device-model-qa"]
                '''
                for t in topics:
                    message = read_kafka(t)
                    print(message)
                '''
                time.sleep(1)
                response_get = requests.get(url=model_url, headers=headers, verify=False)
                if response_get.status_code == 200:
                    response_payload = json.loads(response_get.text)
                    diff = DeepDiff(val_payload, response_payload)

                    if diff=={}:
                        print("validation succeeded")
                        logger.info(f"Validation succeeded")
                    else:
                        print("validation failed")
                        logger.error(f"Validation failed\nDifferences: {diff}")
                        logger.error(f"Response body: {response_get.text}")

                else:
                    logger.error(f"could not fetch the imported device")
                    logger.error(f"error code: {response_get.status_code}\nerror body: {response_get.text}")

            else:
                logger.error(f"Failed to import device {device_name}")
                logger.error(f"Response code: {response.status_code}")
                logger.error(f"Response body: {response.text}")
            #'''

    except Exception as e:
        print(f"Could not perform request action\nException {e}")
        logger.error(f"Could not perform request action {e}")

    finally:
        print("Test completed for import device")
        logger.info("Test completed for import device")

    return

#device_import()