import datetime
import os
import random

from load_dotenv import load_dotenv
import requests
import time
import json
from Requests.Log.logger_setup import setup_log
from deepdiff import DeepDiff
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#set up log file
timestamp=datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir=os.path.join(os.path.dirname(__file__),"Log")
logger=setup_log(os.path.join(log_dir,f"{timestamp}_getModels_by_deviceTypeV2.txt"))

def get_models_device_type_v2():

    print("Test initiated to get particular V2 devices")
    logger.info("Test initiated to get particular V2 devices")


    try:
        with open("config.json","r") as f:
            config = json.load(f)
            url = config["url"]
        token = config["token"]
        devices = config["test_devices"]

        with open("device_deploy.json","r") as f:
            data = json.load(f)

    except Exception as e:
        logger.error("Could not load config.json")


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


    try:
        for m in config['models_v2']:

            model_data = devices[m]
            if model_data=="":
                print(f"device is not created for {m} type")
            else:
                ref_id = "ref"+str(random.randint(1000,9999))
                model_url = f"{url}v2/catalog/models/{model_data}?referenceId={ref_id}"
                print("url: ",model_url)

                response = requests.get(url=model_url, headers=headers, verify=False)
                print(f"response code: {response.status_code}\nresponse text: {response.text}")
                if response.status_code == 200:
                    logger.info(f"Response code: {response.status_code}")
                    logger.info(f"Response body: {response.text}")
                else:
                    logger.error(f"Response code: {response.status_code}")
                    logger.error(f"Response body: {response.text}")
    except Exception as e:
        logger.error("Error during request action")




get_models_device_type_v2()