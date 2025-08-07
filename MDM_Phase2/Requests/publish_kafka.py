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
log_file = os.path.join(log_dir, f"{timestamp}_publish_kafka.ext")
logger = setup_log(log_file, logger_name="file9")

def kafka_v1v2():

    print("Test initiated to publish kafka for v1 and v2 endpoints")
    logger.info("Test initiated to publish kafka for v1 and v2 endpoints")



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


                endpoints = ["v1/fas/publish", "v2/fas/publish"]

                for v in endpoints:

                    vurl = url + v

                    response = requests.post(url=vurl, headers=headers,verify=False)
                    print("Response status code: ", response.status_code)
                    print("Response text: ", response.text)

                    if response.status_code == 200:
                        logger.info(f"Response status code: {response.status_code}")
                        logger.info(f"Response text: {response.text}")


                    else:
                        logger.error(f"Response status code: {response.status_code}")
                        logger.error(f"Response text: {response.text}")


    except Exception as e:
        print("Exception for get device rules: ",e)
        logger.error(f"Exception for get device rules: {e}")

    finally:
        logger.info("Execution to publish kafka for v1 and v2 endpoints completed")
        print("Execution to publish kafka for v1 and v2 endpoints completed")

#kafka_v1v2()