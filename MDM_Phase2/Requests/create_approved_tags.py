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
config_file_path = os.environ.get("CONFIG_PATH")
req_dir_path = os.environ.get("REQ_DIR_PATH")
payload_deploy = os.environ.get("PAYLOAD_DEPLOY")
payload_import = os.environ.get("PAYLOAD_IMPORT")


# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_create_tags.txt")
logger = setup_log(log_file, logger_name="file14")

def create_approved_tags_v2():

    print("test initiated for create approved tags")
    logger.info("Test initiated for create approved tags")

    # Loading the config file
    try:

        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]


    except Exception as e:
        logger.error("Exception occurred during loading config file", e)


    # defining headers:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    try:

        if 'models_v2' in config and 'test_devices' in config:

            for i in config['models_v2']:

                var_tag = "device-class-test-xyz" #this is required parameter for api
                var_value = i #this value for tag will contain devicetype

                model_url=url+"v2/approvedTags?tag="+var_tag+"&value="+var_value

                print("model_url", model_url)
                response_i=requests.post(url=model_url,headers=headers,verify=False)

                if response_i.status_code==201:

                    print(f"Response code for {i}: {response_i.status_code}")
                    print(f"Response for {i}: {response_i.json()}")

                    logger.info(f"Response code {i} model: {response_i.status_code}")
                    logger.info(f"Response text {i} model: {response_i.json()}")

                    #validation
                    val_url = url + "v2/approvedTags"
                    response_v = requests.get(url=val_url, headers=headers, verify=False)

                    if var_tag and var_value in response_v.text:
                        print("Tags are created and validated successfully")
                        logger.info("Tags are created and validated successfully")

                    else:
                        print("Validation failed")
                        logger.error("Validation failed")


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
        print("Test execution completed for creating approved tags")
        logger.info("Test execution completed for creating approved tags")


#create_approved_tags_v2()