import datetime
import copy
import random
import requests
import json
from Requests.Log.logger_setup import setup_log
import os
from load_dotenv import load_dotenv
import urllib3

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
log_file = os.path.join(log_dir, f"{timestamp}_delete_tags.txt")
logger = setup_log(log_file, logger_name="file15")

def delete_approved_tags():

    print("test initiated to delete device tags")
    logger.info("Test initiated to delete device tags")

    #import config file
    try:
        with open (config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]
        print("Config file imported")

    except Exception as e:

        print("Exception occurred while importing the config.json file")
        logger.error("Exception occurred while importing the config.json file")

    #headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        if 'models_v2' in config and 'device_tags' in config:

            for i in config['models_v2']:

                var_value = i
                var_tag = config['device_tags']

                model_url=url+"v2/approvedTags?tag="+var_tag+"&value="+var_value
                response = requests.delete(url=model_url,headers=headers,verify=False)

                print(f"Response code for model {i}: {response.status_code}")
                print(f"Response text for model {i}: {response.text}")

                if response.status_code == 200:

                    logger.info(f"Response code for model {i}: {response.status_code}")
                    logger.info(f"Response text for model {i}: {response.text}")

                    #initiate validation after deletion
                    val_url = url + "v2/approvedTags"
                    response_v = requests.get(url=val_url, headers=headers, verify=False)
                    tags = f'["{var_tag}","{var_value}"]'
                    text = response_v.text.replace(' ','')
                    if tags in text:
                        print("Validation failed")
                        logger.error(f"Validation failed: {response_v.text}")

                    else:
                        print(f"tags are deleted successfully and validated")
                        logger.info(f"tags are deleted successfully and validated: {response_v.text}")

                else:

                    logger.error(f"Response code for model {i}: {response.status_code}")
                    logger.error(f"Response text for model {i}: {response.text}")
        else:
            print("models/devices not present in config file")
            logger.error("models/devices not present in config file")

    except Exception as e:
        print("Exception occurred while deleting device: ",e)
        logger.error(f"Exception occurred while device device: {e}")

    finally:
        print("Test completed for removing the device")
        logger.info(f"Test completed for removing the device")




#delete_approved_tags()