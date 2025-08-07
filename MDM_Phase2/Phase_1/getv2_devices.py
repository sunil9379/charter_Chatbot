import json
import random
import datetime
import os
import requests
from load_dotenv import load_dotenv
from Phase_1.log_setup import setup_log
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")

def get_call(req_dir_path,log_name,flow=None):

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_{log_name}.txt")
    logger = setup_log(log_file, logger_name="file1")

    logger.info("Test initiated to get v2 devices")
    with open(config_file_path,"r") as f:
        config = json.load(f)

    url = config["url"]
    token = config["token"]
    payload = config['test_devices']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    results = {}
    for m in config['models_v2']:

        device = payload[m]
        ref_id = str(random.randint(1000,9999))
        model_url = f"{url}v2/catalog/models/{device}?referenceId={ref_id}"
        #print("get url: ",model_url)

        logger.info(f"Getting response for device {device}")
        response = requests.get(url=model_url, headers=headers,verify=False)
        rcode = response.status_code
        rbody = response.text

        if flow=="call2":
            if rcode == 404:
                logger.info("Received required response")
                logger.info(f"Code: {rcode}\nBody: {rbody}")
                print(f"Received required response\nCode: {rcode}\nBody: {rbody}")
            else:
                logger.error("Received invalid response")
                logger.error(f"Code: {rcode}\nBody: {rbody}")
                print(f"Received required response\nCode: {rcode}\nBody: {rbody}")
        else:
            if rcode == 200:
                logger.info(f"Getting success response for device {device}")
                logger.info(f"Success code: {rcode}\nResponse Body: {rbody}")
                print(f"Success response for device {device}\ncode: {rcode}\nbody: {rbody}")

                if device in response.text:
                    logger.info(f"Device {device} present in response body")
                    print(f"Device {device} present in response body")
                else:
                    logger.error(f"Device {device} is not present in response body")
                    print(f"Device {device} is not present in response body")
            else:
                logger.error(f"Getting failure response for device {device}")
                logger.error(f"Error code: {rcode}\nResponse Body: {rbody}")
                print(f"Error response for device {device}\ncode: {rcode}\nbody: {rbody}")



        #results[device] = rcode
    return response