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
config_file_path = os.environ.get("CONFIG_PATH") #this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH") #this is Requests directory path

#set up log file
timestamp=datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir=os.path.join(os.path.dirname(__file__),f"{req_dir_path}Log")
logger=setup_log(os.path.join(log_dir,f"{timestamp}_certify_device.text"))

def certify_device():

    print("test initiated to certify device")
    logger.info("Test initiated to certify device")

    #import config file and payload file
    try:
        with open (config_file_path,"r") as f:
            config = json.load(f)
        print("Config file imported")

        with open("certify_payload.json","r") as f:
            payload = json.load(f)
        print("Payload file imported")

    except Exception as e:

        print("Exception occurred while importing the config.json or certify_payload.json file")
        logger.error("Exception occurred while importing the config.json or certify_payload.json file")

    #headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['token']}"
    }

    try:
        if 'test_devices' in config:

            devices = config['test_devices']
            data = copy.deepcopy(payload)
            payload_keys = data.keys()

            for device in devices:

                if device in payload_keys:
                   value_present = data[device] #this is a value(json payload) of particular device
                   #print(value_present)

                   for k,v in data.items():
                       for key, value in v.items():
                           if value == "xyz":
                               v[key] = devices[device]
                           elif 'xyz' in value:
                               v[key] = value.replace('xyz',devices[device])


                else:
                    pass





    except Exception as e:
        print("Exception occurred while creating device: ",e)
        logger.error(f"Exception occurred while creating device: {e}")

    finally:
        print("Test completed for pushing device in test stage")
        logger.info(f"Test completed for pushing device in test stage")




certify_device()