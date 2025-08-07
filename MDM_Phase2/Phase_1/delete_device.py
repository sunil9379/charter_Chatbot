import random
import os
import json
import datetime
import requests
from Phase_1.log_setup import setup_log
from dotenv import load_dotenv

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")

def delete_devices(req_dir_path,log_name,flow=None):

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_{log_name}.txt")
    logger = setup_log(log_file, logger_name="file1")

    with open(config_file_path, "r") as f:
        config = json.load(f)
    url = config["url"]
    token = config["token"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    for m in config["models_v2"]:

        device = config['test_devices'][m]
        ref_id = "sd" + str(random.randint(1000, 9999))

        url_model = url + "v2/catalog/models/" + device + "?referenceId=" + ref_id + "&userId=P3289462"

        response = requests.delete(url=url_model, headers=headers, verify=False)
        print("Response code: ", response.status_code)
        print("Response body: ", response.text)

        if flow=="call2":
            if response.status_code == 404:
                logger.info("Received required response")
                logger.info(f"Code: {response.status_code}\nBody: {response.text}")
                print(f"Received required response\nCode: {response.status_code}\nBody: {response.text}")
            else:
                logger.error("Received invalid response")
                logger.error(f"Code: {response.status_code}\nBody: {response.text}")
                print(f"Received required response\nCode: {response.status_code}\nBody: {response.text}")
        else:
            if response.status_code == 204:
                logger.info(f"Device {device} successfully deleted")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Response body: {response.text}")
            else:
                logger.error(f"Device {device} failed to delete")
                logger.error(f"Response code: {response.status_code}")
                logger.error(f"Response body: {response.text}")



