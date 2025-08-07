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
config_file_path = os.environ.get("CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH")  # this is Requests directory path
payload_deploy = os.environ.get("PAYLOAD_DEPLOY")
payload_import = os.environ.get("PAYLOAD_IMPORT")


# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_get_aggregate.txt")
logger = setup_log(log_file, logger_name="file2")
#logger = setup_log(os.path.join(log_dir, f"{timestamp}_get_aggregate_view.text"))

def aggregate_view():
    '''
        Test for v1 endpoint
    '''
    print("Test initiated for aggregate view v1")
    logger.info("Test initiated for aggregate view v1")

    # importing the payload and config file:
    try:
        print("importing the payload file")

        with open(payload_import, "r") as f:
            data = json.load(f)
            payload = copy.deepcopy(data)

        with open(config_file_path, "r") as f:
            config = json.load(f)
        url = config['url']
        token = config['token']
        logger.info("Imported the payload and config file")

    except Exception as e:
        logger.error(f"Failed to import the json files: {e}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        for m in config["models_v2"]:

            #defining device level details
            device_payload = payload[m]
            device_name = device_payload.get('data')[0].get('modelName')
            vendor_name = device_payload.get('data')[0].get('vendorName')
            firmware_edva = device_payload.get('data')[0].get('firmwareDesc',{}).get('eDvaFirmware')
            firmware_tag_bhn = device_payload.get('data')[0].get('firmwareDesc',{}).get('firmwareVersions',[{}])[0].get('firmwareTags').get('bhn')
            firmware_tag_bhn_keys = firmware_tag_bhn.keys()
            firmware_tag_bhn_value = firmware_tag_bhn.values()
            firmware_tag_twc = device_payload.get('data')[0].get('firmwareDesc',{}).get('firmwareVersions',[{}])[0].get('firmwareTags').get('twc')
            firmware_tag_twc_keys = firmware_tag_twc.keys()
            firmware_tag_twc_value = firmware_tag_twc.values()
            firmware_key = vendor_name+"|"+device_name +"|" +firmware_edva
            print("KEY: ",firmware_key)
            print("device details fetched")

            v1_url = f"{url}v1/legacy/aggregateView?vendor={vendor_name}&model={device_name}&firmware={firmware_edva}"
            v2_url = f"{url}v2/legacy/aggregateView?vendor={vendor_name}&model={device_name}&firmware={firmware_edva}"
            print("v1 v2 url fetched",f"\n{v1_url}\n{v2_url}")

            logger.info("============================================")
            logger.info(f"Initiating request action for {device_name}")

            logger.info("***************************")
            logger.info("for v1 endpoints")
            response_v1 = requests.get(v1_url, headers=headers, data=json.dumps(device_payload), verify=False)
            print("Response code: ",response_v1.status_code)
            print("Response body: ",response_v1.text)


            if response_v1.status_code == 200:
                logger.info("Api run Success")
                logger.info(f"V1 Response code: {response_v1.status_code}")
                logger.info(f"V1 Response body: {response_v1.text}")

                response_data = response_v1.json()
                twc_tag = response_data['base']['twc'][firmware_key]
                bhn_tag = response_data['base']['bhn'][firmware_key]

                val_status = False
                logger.info("Validation for v1")
                for k1,v1 in zip(firmware_tag_bhn_keys,firmware_tag_bhn_value):
                    if k1 in bhn_tag and v1 in bhn_tag:
                        #print(f"The key {k1} has value {v1} in response payload")
                        val_status = True

                    else:
                        #print(f"{k1}/{v1} not in bhn tag of response payload")
                        val_status = False

                if val_status == True:
                    print("Validation for bhn tag succeeded")
                    logger.info(f"Validation for bhn tag of {device_name} succeeded at v1 ")
                else:
                    print("Failed to validate bhn tag")
                    logger.error(f"Validation for bhn tag of {device_name} failed at v1 ")

                for k1,v1 in zip(firmware_tag_twc_keys,firmware_tag_twc_value):
                    if k1 in twc_tag and v1 in twc_tag:
                        #print(f"The key {k1} has value {v1} in response payload")
                        val_status = True

                    else:
                        #print(f"{k1}/{v1} not in twc tag of response payload")
                        val_status = False

                if val_status == True:
                    print("Validation for twc succeeded")
                    logger.info(f"Validation for twc tag of {device_name} succeeded at v1")
                else:
                    print("Failed to validate twc tag")
                    logger.error(f"Validation for twc tag of {device_name} failed at v1")

            else:
                logger.error(f"V1 Response code: {response_v1.status_code}\nV1 Response Body: {response_v1.text}")


            logger.info("***************************\nFor v2 endpoint")
            response_v2 = requests.get(v2_url, headers=headers, data=json.dumps(device_payload), verify=False)
            print("Response code: ",response_v2.status_code)
            print("Response body: ",response_v2.text)


            if response_v2.status_code == 200:
                logger.info("Api run Success")
                logger.info(f"V2 Response code: {response_v2.status_code}")
                logger.info(f"V2 Response body: {response_v2.text}")

                response_data = response_v2.json()
                twc_tag = response_data['base']['twc'][firmware_key]
                bhn_tag = response_data['base']['bhn'][firmware_key]

                val_status = False
                logger.info("Validation for v2")
                for k2, v2 in zip(firmware_tag_bhn_keys, firmware_tag_bhn_value):
                    if k2 in bhn_tag and v2 in bhn_tag:
                        # print(f"The key {k1} has value {v1} in response payload")
                        val_status = True

                    else:
                        # print(f"{k1}/{v1} not in bhn tag of response payload")
                        val_status = False

                if val_status == True:
                    print("Validation for bhn tag succeeded")
                    logger.info(f"Validation for bhn tag of {device_name} succeeded at v2 ")
                else:
                    print("Failed to validate bhn tag")
                    logger.error(f"Validation for bhn tag of {device_name} failed at v2")

                for k2, v2 in zip(firmware_tag_twc_keys, firmware_tag_twc_value):
                    if k2 in twc_tag and v2 in twc_tag:
                        # print(f"The key {k1} has value {v1} in response payload")
                        val_status = True

                    else:
                        # print(f"{k1}/{v1} not in twc tag of response payload")
                        val_status = False

                if val_status == True:
                    print("Validation for twc succeeded")
                    logger.info(f"Validation for twc tag of {device_name} succeeded at v2")
                else:
                    print("Failed to validate twc tag")
                    logger.error(f"Validation for twc tag of {device_name} failed at v2")



            else:
                logger.error(f"V2 Response code: {response_v2.status_code}")
                logger.error(f"V2 Response body: {response_v2.text}")


    except Exception as e:
        print("Failed to initiate request")
        logger.error("Exception caused while request: ",e)

#aggregate_view()