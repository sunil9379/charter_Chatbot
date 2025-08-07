import time
from Phase_1.getfirmwareinfo import get_firmware_infov1,get_firmware_infov2
from Phase_1.getallfirmwares import firmwares_v1,firmwares_v2
import os
import json
import datetime
import random
import requests
from Phase_1.log_setup import setup_log
from dotenv import load_dotenv

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")
req_dir_path = os.environ.get("P1_CERTIFY_LOG_PATH")


def certify_put_firmware_version():

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_put_firmware_version.txt")
    logger = setup_log(log_file, logger_name="file0")

    print("Test initiated to update firmware version")
    logger.info("Test initiated to update firmware version")

    with open(config_file_path, "r") as f:
        config = json.load(f)
    url = config["url"]
    token = config["token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        for m in config["models_v2"]:

            payload = config["post_firmware"]
            model_name = config["test_devices"][m]
            firmware_version = f"{model_name}-P20-040625-2025.5"
            firmwaretp = "HTTPS"
            ref_id = model_name + str(random.randint(1000, 9999))
            ext_id = model_name + str(random.randint(1000, 9999))

            payload["firmwareVersion"] = f"{model_name}-P20-040625-2025.6"
            payload["firmwareFilename"] = payload['firmwareVersion'] + ".charter"
            payload["firmwareTransferProtocol"] = firmwaretp
            payload["metadata"]["referenceId"] = ref_id
            payload["metadata"]["externalId"] = ext_id

            murl = f"{url}v2/catalog/models/{model_name}/firmwares/{firmware_version}"
            logger.info(f"Updating the firmware for device {model_name} and firmware {firmware_version}")
            resp = requests.put(url=murl, json=payload, headers=headers, verify=False)


            if resp.status_code == 201:
                print(f"Firmware {firmware_version} updated successfully\nstatus code: {resp.status_code}\nresponse: {resp.text}")
                logger.info(f"Firmware {firmware_version} updated successfully\nstatus code: {resp.status_code}\nresponse: {resp.text}")

                config["updated_certify_firmwares"][m] = payload["firmwareVersion"]
                with open(config_file_path, "w") as f:
                    json.dump(config,f,indent=4)

            else:
                print(f"Firmware {firmware_version} update failed\nstatus code: {resp.status_code}\nresponse: {resp.text}")
                logger.error(f"Firmware {firmware_version} update failed\nstatus code: {resp.status_code}\nresponse: {resp.text}")
    except Exception as e:
        print(f"Exception caused during request action: {e}")
        logger.error(f"Exception caused during request action: {e}")

    finally:
        print("Test completed to update firmware version")


'''
GET FIRMWARE DETAILS
'''

def put_get_all_firmwaresv1():

    with open(config_file_path) as f:
        config = json.load(f)
    data = config["updated_certify_firmwares"]
    response,logger = firmwares_v1(req_dir_path,"updated_get_firmwares_v1")
    logger.info("Start of Validation")

    try:
        for key,value in data.items():
            if value in response[key]:
                print(f"firmware {value} present in response")
                logger.info(f"Firmware {value} present in response")
            else:
                print(f"firmware {value} not present in response")
                logger.error(f"firmware {value} not present in response")
    except Exception as e:
        print(e)
    finally:
        print("Test Completed for get all firmwares v1")

def put_get_all_firmwaresv2():

    with open(config_file_path) as f:
        config = json.load(f)
    data = config["updated_certify_firmwares"]
    response,logger = firmwares_v2(req_dir_path,"updated_get_firmwares_v2")
    logger.info("Start of Validation")

    try:
        for key,value in data.items():
            if value in response[key]:
                print(f"firmware {value} present in response")
                logger.info(f"Firmware {value} present in response")
            else:
                print(f"firmware {value} not present in response")
                logger.error(f"firmware {value} not present in response")
    except Exception as e:
        print(e)
    finally:
        print("Test Completed for get all firmwares v2")




'''
GET FIRMWARE INFO
'''

def put_get_firmware_info_v1():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_updated_firmware_info_v1.txt")
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
            if result["Status Code"]==200:
                print(f"Success response received")
                print(result["Response Body"])
                logger.info(f"Success response received")
                logger.info(f"Success Code: 200")
                logger.info(f"Response Message: {result['Response Body']}")
            else:
                print(f"Failed response received")
                print(result["Response Body"])
                logger.error(f"Error Code: {result['Status Code']}")
                logger.error(f"Response Body: {result['Response Body']}")
    except Exception as e:
        print(f"Exception occurred while request action: {e}")
    finally:
        print("Test completed for get firmware info v1")

def put_get_firmware_info_v2():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_updated_firmware_info_v2.txt")
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

            logger.info(f"Getting v1 firmware info for device {value},firmware {firmware}")
            print(f"getting v1 firmware info for device {value},firmware {firmware}")
            if result["Status Code"]==200:
                print(f"Success response received")
                print(result["Response Body"])
                logger.info(f"Success response received")
                logger.info(f"Success Code: 200")
                logger.info(f"Response Message: {result['Response Body']}")
            else:
                print(f"Failed response received")
                print(result["Response Body"])
                logger.error(f"Error Code: {result['Status Code']}")
                logger.error(f"Response Body: {result['Response Body']}")
    except Exception as e:
        print(f"Exception occurred while request action: {e}")
    finally:
        print("Test completed for get firmware info v2")

#put_get_firmware_info_v1()
#time.sleep(2)
#put_get_firmware_info_v2()