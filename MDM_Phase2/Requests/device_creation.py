import copy
import random
import time

import requests
import json
import urllib3
from dotenv import load_dotenv
import os
import datetime
from Log.logger_setup import setup_log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH")  # this is Requests directory path

# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
logger = setup_log(os.path.join(log_dir, f"{timestamp}_device_creation.text"))

def device_test():

    logger.info("-------------------------------**----------------------------")
    print("Test initiated to create device in test stage")
    logger.info("Test initiated to create device in test stage")

    #importing the payload and config file:
    try:
        print("importing the payload file")

        with open("device_test.json","r") as f:
            data = json.load(f)
            payload = copy.deepcopy(data)

        with open("config.json","r") as f:
            content = json.load(f)
            url = content['url']
            token = content['token']
        logger.info("Imported the payload and config file")

    except Exception as e:
        logger.error(f"Failed to import the json files: {e}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in content['models_v2']:

                data_model = payload[m]
                url_m = url + "v2/catalog/models"
                ref_id = str(random.randint(1000,9999))
                ext_id = str(random.randint(1000,9999))

                data_model['metadata']['referenceId'] = ref_id
                data_model['metadata']['externalId'] = ext_id
                model_name = data_model['modelName']

                response = requests.post(url=url_m, headers = headers, json=data_model, verify=False)
                print("Response code: ",response.status_code)
                print("Response body: ",response.text)

                logger.info("======================================================")

                if response.status_code == 201:
                    print("Device created in test stage successfully")
                    logger.info(f"Device created for {m} in test stage successfully\nResponse Body: {response.text}")

                    content['test_devices'][m] = model_name
                    with open(config_file_path,"w") as f:
                        json.dump(content,f, indent=4)

                else:
                    print("Device creation in test stage failed")
                    logger.error(f"Failed to create {m} device in test stage\nResponse Body: {response.text}")


    except Exception as e:
        print("Exception occurred in request action")
        logger.error(f"Exception occurred in request action: {e}")

    finally:
        print("Test completed for test stage")
        logger.info("Test completed for test stage")


'''
The device created in test stage will be pushed to certify
'''



def device_certify():
    logger.info("-------------------------------**----------------------------")
    print("Pushing the device from test to certify stage")
    logger.info("Pushing the device from test to certify stage")

    # importing the payload and config file:
    try:
        print("importing the payload file")

        with open("device_certify.json", "r") as f:
            data = json.load(f)
            payload = copy.deepcopy(data)

        with open("config.json", "r") as f:
            content = json.load(f)
            url = content['url']
            token = content['token']
        logger.info("Imported the payload and config file")

    except Exception as e:
        logger.error(f"Failed to import the json files: {e}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in content['models_v2']:

            data_model = payload[m]
            #time.sleep(5)
            print(f"Payload for {m} device: {data_model}")
            device_name = content['test_devices'][m]

            device_url = url + "v2/catalog/models/" + device_name + "?status=Certified"
            print("device url: ",device_url)
            logger.info(f"device url: {device_url}")
            logger.info(f"data model: {data_model}")

            response = requests.put(url=device_url, headers=headers, json=data_model, verify=False)
            print("Response code: ",response.status_code)
            print("Response body: ",response.text)

            logger.info("======================================================")

            if response.status_code == 201:
                logger.info(f"Device {device_name} successfully pushed to certify stage")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Response body: {response.text}")

            else:
                logger.error(f"Device {device_name} failed to push to certify stage")
                logger.error(f"Error code: {response.status_code}")
                logger.error(f"Error message: {response.text}")
    except Exception as e:
        print(f"Failed to perform request action: {e}")


'''
Push device from certified to deploy stage
'''

def device_deploy():
    logger.info("-------------------------------**----------------------------")
    print("Pushing the device from certify to deploy stage")
    logger.info("Pushing the device from certify to deploy stage")

    # importing the payload and config file:
    try:
        print("importing the payload file")

        with open("device_deploy.json", "r") as f:
            data = json.load(f)
            payload = copy.deepcopy(data)

        with open("config.json", "r") as f:
            content = json.load(f)
            url = content['url']
            token = content['token']
        logger.info("Imported the payload and config file")

    except Exception as e:
        logger.error(f"Failed to import the json files: {e}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in content['models_v2']:

            data_model = payload[m]
            #time.sleep(5)
            print(f"Payload for {m} device: {data_model}")
            device_name = content['test_devices'][m]

            device_url = url + "v2/catalog/models/" + device_name + "?status=Deploy"

            response = requests.put(url=device_url, headers=headers, json=data_model, verify=False)
            print("Response code: ", response.status_code)
            print("Response body: ", response.text)

            logger.info("======================================================")
            if response.status_code == 201:
                logger.info(f"Device {device_name} successfully pushed to deploy stage")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Response body: {response.text}")

            else:
                logger.error(f"Device {device_name} failed to push to deploy stage")
                logger.error(f"Error code: {response.status_code}")
                logger.error(f"Error message: {response.text}")

    except Exception as e:
        print(f"Failed to perform request action: {e}")


def delete_devices():
    with open("config.json", "r") as f:
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

        if response.status_code == 204:
            logger.info(f"Device {device} successfully deleted")
            logger.info(f"Response code: {response.status_code}")
            logger.info(f"Response body: {response.text}")
        else:
            logger.error(f"Device {device} failed to delete")
            logger.error(f"Response code: {response.status_code}")
            logger.error(f"Response body: {response.text}")

#'''
device_test()
time.sleep(5)
device_certify()
time.sleep(5)
#device_deploy()
#'''
#delete_devices()