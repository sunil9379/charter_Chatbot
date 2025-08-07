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
#req_dir_path = os.environ.get("P1_TEST_LOG_PATH")

def get_matched_v2(req_dir_path,log_name,stage):

    # set up log file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_{log_name}.txt")
    logger = setup_log(log_file, logger_name="file1")

    print("Test initiated get all matched models")
    logger.info("Test initiated get all matched models")

    with open(config_file_path,"r") as f:
        config = json.load(f)
    url = config["url"]
    token = config["token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in config["models_v2"]:
            dtype = m
            ref_id = "sd" +str(random.randint(100,999))
            device_name = config["test_devices"][m]
            murl = f"{url}v2/catalog/models?status={stage}&device_type={dtype}&referenceId={ref_id}"

            response = requests.get(url=murl, headers=headers, verify=False)
            print("response code: ", response.status_code)
            print("response text: ", response.text)
            if response.status_code == 200:
                logger.info("Success response")
                logger.info(f"Success code: {response.status_code}\nResponse Body: {response.text}")

                if device_name in  response.text:
                    print(f"{device_name} found in response")
                    logger.info(f"{device_name} found in response. Validation success")
                else:
                    print(f"{device_name} not found in response ")
                    logger.error(f"{device_name} not found in response. Validation failed")
            else:
                logger.error("Failed to get response ")
                logger.error(f"Error code: {response.status_code}\nResponse Body: {response.text}")

    except Exception as e:
        logger.error(f"Exception occurred while  request action: {e}")
        print(f"Exception occurred while  request action: {e}")

#get_matched_v2(req_dir_path)