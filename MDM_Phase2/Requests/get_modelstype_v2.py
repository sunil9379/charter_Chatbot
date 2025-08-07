import datetime
import os
import random
import requests
import time
import json
from Log.logger_setup import setup_log
from deepdiff import DeepDiff
import urllib3
from Utils.create_device_test import create_test_device

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#set up log file
timestamp=datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir=os.path.join(os.path.dirname(__file__),"Log")
logger=setup_log(os.path.join(log_dir,f"{timestamp}_v2get_modelstype.txt"))

def get_models_types_v2():

    #creating the device in test stage
    create_device = create_test_device()

    print("test initiated for get device types by models v2")
    logger.info("Test initiated for get device types by models v2")

    # get access token:
    try:

        with open('access_token.txt', 'r') as f:
            token = f.read()
        logger.info("Token loaded")
        print("Token loaded")

    except Exception as e:
        logger.error(e)
        print("Error occurred ", e)

    # defining headers:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Loading the config file
    try:

        with open("config.json") as f:
            config = json.load(f)

        # importing the base url
        if "url" in config:
            url = config["url"]

        else:
            print("url not present in config.json")
            logger.error("url not present in config.json")

    except Exception as e:
        logger.error("Exception occurred during loading config file", e)

    #Generate random reference id
    ref_id = str(random.randint(1000,9999))
    ref_id = 'Atmn_' + ref_id

    try:

        if 'models_v2' in config and 'test_devices' in config:

            for i in config['models_v2']:

                model_url=url+"v2/catalog/deviceTypes/"+i+"?referenceId="+ref_id
                print("model_url", model_url)
                response_i=requests.get(url=model_url,headers=headers,verify=False)

                if response_i.status_code==200:

                    print(f"Response code for {i}: {response_i.status_code}")
                    print(f"Response for {i}: {response_i.json()}")

                    logger.info(f"Response code {i} model: {response_i.status_code}")
                    logger.info(f"Response text {i} model: {response_i.json()}")

                    #validation
                    if i in config['test_devices']:

                        model_name = config['test_devices'][i]

                        if model_name in response_i.text:
                            print("Device created is present in Get device types v2 api")
                            logger.info("Device present, Validation SUCCESS")
                        else:
                            print("Device NOT present in Get device types v2 api")
                            logger.error("Device not present, Validation FAILED")


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
        print("Test execution completed for get models type v2")
        logger.info("Test execution completed for get models type v2")


get_models_types_v2()