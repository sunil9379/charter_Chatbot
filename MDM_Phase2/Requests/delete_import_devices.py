import datetime
import copy
import random
import time

import requests
import json
from Requests.Log.logger_setup import setup_log
import os
from load_dotenv import load_dotenv
import urllib3
from getv2_devices import get_call

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH") #this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH") #this is Requests directory path

#set up log file
timestamp=datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir=os.path.join(os.path.dirname(__file__),f"{req_dir_path}Log")
logger=setup_log(os.path.join(log_dir,f"{timestamp}_delete_imported_devices.txt"))

def delete_import():

    print("test initiated to delete device in import stage")
    logger.info("Test initiated to delete device in import stage")

    # import config file
    try:
        with open(config_file_path, "r") as f:
            config = json.load(f)
        url = config["url"]
        print("Config file imported")

    except Exception as e:

        print("Exception occurred while importing the config.json file")
        logger.error("Exception occurred while importing the config.json file")

    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['token']}"
    }
    deleted_devices = []

    #get_api = get_call()
    try:

        if 'models_v2' in config and 'imported_devices' in config:
            for i in config['models_v2']:
                model_name = config['imported_devices'][i]
                random_ref_id = str(random.randint(1000, 9999))
                user_id = "P3289462"

                model_url = url + 'v2/catalog/models/' + model_name + '?referenceId=/' + random_ref_id + "&userId=" + user_id
                response = requests.delete(url=model_url, headers=headers, verify=False)

                print(f"Response code for model {model_name}: {response.status_code}")
                print(f"Response text for model {model_name}: {response.text}")

                if response.status_code == 204:

                    logger.info(f"Response code for model {model_name}: {response.status_code}")
                    logger.info(f"Response text for model {model_name}: {response.text}")

                    time.sleep(5)
                    #validating by get call:
                    result = get_call("imported_devices")
                    if model_name in result:
                        if result[model_name] == 200:
                            print("Model still present")
                        else:
                            print("Model deleted")
                            deleted_devices.append(i)

                    else:
                        print(f"{model_name} is not present in the imported devices")


                elif response.status_code == 500 or response.status_code == 503:
                    time.sleep(3)
                    retry_response = requests.delete(url=model_url, headers=headers, verify=False)
                    if retry_response.status_code == 204:
                        logger.info(f"Code: {retry_response.status_code}")
                        logger.info(f"Response text for model {model_name}: {retry_response.text}")
                        deleted_devices.append(i)
                    else:
                        logger.error("retry to delete the model failed")
                        deleted_devices.append(i)
                else:

                    logger.error(f"Response code for model {model_name}: {response.status_code}")
                    logger.error(f"Response text for model {model_name}: {response.text}")
        else:
            print("models/devices not present in config file")
            logger.error("models/devices not present in config file")

    except Exception as e:
        print("Exception occurred while deleting device: ", e)
        logger.error(f"Exception occurred while device device: {e}")

    finally:
        for i in deleted_devices:
            config['imported_devices'][i] = ""

        with open(config_file_path, "w") as f:
            json.dump(config, f, indent=4)
        print("Test completed for removing the device")
        logger.info(f"Test completed for removing the device")


delete_import()