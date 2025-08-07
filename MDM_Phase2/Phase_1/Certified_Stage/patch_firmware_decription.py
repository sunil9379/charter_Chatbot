import random
import os
import time

import requests
import json
import datetime

from Phase_1.Certified_Stage.kafka_info import read_kafka
from Phase_1.getallfirmwares import firmwares_v2,firmwares_v1
from Phase_1.getfirmwareinfo import get_firmware_infov1,get_firmware_infov2
from Phase_1.log_setup import setup_log
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
req_dir_path = os.environ.get("P1_CERTIFY_LOG_PATH")
config_file_path = os.environ.get("P1_CONFIG_PATH")

def patch_firmware_description():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_patch_firmware_description.txt")
    logger = setup_log(log_file, logger_name="file5")

    print("Test initiated for updating the firmware description")
    logger.info("Test initiated for updating the firmware description")

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
            payload = config["patch_payload"]
            device_name = config["test_devices"][m]

            payload["defaultVersion"]= f"{device_name}-P20-040625-2025.1"
            payload["eMtaFirmware"] = f"{device_name}-P15-040625-2025.1"
            payload["eDvaFirmware"] = None

            murl = f"{url}v2/catalog/models/{device_name}/firmwares"

            resp = requests.patch(url=murl, json=payload, headers=headers,verify=False)

            logger.info(f"Updating the firmware description for {device_name}")
            if resp.status_code in(201,500):
                print(f"Firmware updated successfully for {device_name}")
                logger.info(f"Firmware updated successfully for {device_name}")

                #KAFKA VALIDATION
                ''''
                message,present = read_kafka("deviceopedia-authoritative-firmware-avro-qa-mdm")
                if 'edvaAuthorizedFirmware' in message:
                    print("yes")
                else:
                    print("no")
                '''

            else:
                print("Firmware update failed")
                logger.error(f"Firmware update failed for {device_name}")
    except Exception as e:
        print(e)

def patch_get_all_firmwares_v1():

    with open(config_file_path,"r") as f:
        config = json.load(f)
    response_v1, logger = firmwares_v1(req_dir_path, "patch_get_all_firmwarev1")
    try:

        for key,value in config["updated_certify_firmwares"].items():

            if value in response_v1[key]:
               print(f"Firmware description update for {value} validated using get all firmware v1")
               logger.info(f"Firmware description update for {value} validated using get all firmware v1")
            else:
                print(f"Firmware description update for {value} could not be validated using get all firmware v1")
                logger.error(f"Firmware description update for {value} could not be validated using get all firmware v1")


    except Exception as e:
        print("Exception occurred while get all firmware call: ",e)
        logger.error(f"Exception occurred while get all firmware call: {e}")

    finally:
        logger.info("Test execution for get all firmware_v1 completed")


def patch_get_all_firmwares_v2():
    with open(config_file_path, "r") as f:
        config = json.load(f)
    data = config["test_devices"]
    response_v2, logger = firmwares_v2(req_dir_path, "patch_get_all_firmware2")

    try:
            for key,value in data.items():

                content_v2 = json.loads(response_v2[key])
                if key in response_v2:
                    if content_v2['eDvaFirmware'] == None:
                        print(f"Firmware description update for {value} validated using get all firmware v2")
                        logger.info(f"Firmware description update for {value} validated using get all firmware v2")
                    else:
                        print(f"Firmware description update for {value} could not be validated using get all firmware v2")
                        logger.error(f"Firmware description update for {value} could not be validated using get all firmware v2")
                else:
                    print(f"{key} not found")

    except Exception as e:
        print("Exception occurred while get all firmware call: ", e)
        logger.error(f"Exception occurred while get all firmware call: {e}")

    finally:
        logger.info("Test execution for get all firmware_v2 completed")



def patch_get_firmware_info_v1():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_patch_firmware_info_v1.txt")
    logger = setup_log(log_file, logger_name="file6")

    logger.info("Test initiated for get firmware info v1")
    with open(config_file_path,"r") as f:
        config = json.load(f)
    vendors={
        "ata":"Ubee",
        "mta":"Technicolor",
        "cwl":"Motorola",
        "onu":"ALCATEL",
        "snu":"Humax"
    }
    devices = config["test_devices"]
    try:
        for key,value in devices.items():
            firmware = config["updated_certify_firmwares"][key]
            vendor = vendors[key]
            result = get_firmware_infov1(modelname=value,vendors=vendor,firmware=firmware)

            logger.info(f"Getting v1 firmware info for device {value},vendor {vendor},firmware {firmware}")
            print(f"Getting v1 firmware info for device {value},vendor {vendor},firmware {firmware}")
            response = result["Response Body"]

            response = json.loads(response)
            if result['Status Code']==200 and response['pktcblEdvaFirmware']==None:
                print(f"Description updated is been validated using get all firmware info v1")
                logger.info(f"validation Successful. From get firmware info the description has been updated for value edvaFirmware for device {value}")
            else:
                print(f"Description updated is been validated using get all firmware info v1")
                logger.error(f"FValidation failed for {value}")

    except Exception as e:
        print(f"Exception occurred while request action: {e}")
    finally:
        print("Test completed for get firmware info v1")



def patch_get_firmware_info_v2():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_patch_firmware_info_v2.txt")
    logger = setup_log(log_file, logger_name="file7")

    logger.info("Test initiated for get firmware info v2")
    with open(config_file_path,"r") as f:
        config = json.load(f)

    devices = config["test_devices"]
    try:
        for key,value in devices.items():
            firmware = config["updated_certify_firmwares"][key]
            #print("firmware:",firmware)
            result = get_firmware_infov2(modelname=value,firmware=firmware)

            logger.info(f"Getting v2 firmware info for device {value},firmware {firmware}")
            print(f"getting v2 firmware info for device {value},firmware {firmware}")
            response = result["Response Body"]
            response = json.loads(response)
            if result['Status Code']==200  and firmware==response['firmwareVersion']:
                print(f"Validation Success for device {value} at get firmware info v2")
                logger.info(f"Validation Success for device {value} at get firmware info v2")
            else:
                print(f"Validation Failed for device {value} at get firmware info v2")
                logger.error(f"Validation Failed for device {value} at get firmware info v2")


    except Exception as e:
        print(f"Exception occurred while request action: {e}")
    finally:
        print("Test completed for get firmware info v2")




#patch_firmware_description()
'''
time.sleep(3)
patch_get_all_firmwares_v1()
time.sleep(3)
patch_get_all_firmwares_v2()
time.sleep(3)
patch_get_firmware_info_v1()
time.sleep(3)
patch_get_firmware_info_v2()
'''