import copy
import random
import time
from dotenv import load_dotenv
import os
import datetime
import requests
import json
import urllib3
from Phase_1.log_setup import setup_log
from Phase_1.getallfirmwares import firmwares_v1,firmwares_v2
from Phase_1.getfirmwareinfo import get_firmware_infov1,get_firmware_infov2
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")
req_dir_path = os.environ.get("P1_DEPLOY_LOG_PATH")
payload_certify = os.environ.get("P1_DEPLOY_PAYLOAD")

# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_create_deploy_firmwares.txt")
logger = setup_log(log_file, logger_name="file4")

def deploy_create_firmware():
    print("Test initiated for creating firmware")
    logger.info("Test initiated for creating firmware")

    with open(config_file_path, "r") as f:
        config = json.load(f)
        data = config["post_firmware"]
    url = config["url"]
    token = config["token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        for m in config["models_v2"]:
            payload = copy.deepcopy(data)
            devices = config["test_devices"][m]
            murl = f"{url}v2/catalog/models/{devices}/firmwares"

            firmwareversion = f"{devices}-P15-040625-2025.5"
            firmware_filename = f"{firmwareversion}.charter"
            firmwaretp = "HTTPS"
            ref_id = devices + str(random.randint(1000,9999))
            ext_id = devices + str(random.randint(1000,9999))

            payload['firmwareVersion'] = firmwareversion
            payload['firmwareFilename'] = firmware_filename
            payload['firmwareTransferProtocol'] = firmwaretp
            payload['metadata']['externalId'] = ext_id
            payload['metadata']['referenceId'] = ref_id

            print(payload)
            logger.info(f"Payload: {payload}")
            #print(murl)
            time.sleep(3)
            response = requests.post(url=murl, json=payload, headers=headers,verify=False)

            if response.status_code == 201:
                print("Firmware created successfully")
                logger.info(f"Firmware for {devices} created successfully")
                logger.info(f"Success Code: {response.status_code}")
                logger.info(f"Response Message: {response.text}")

                config["deploy_firmwares"][m] = firmwareversion
                with open(config_file_path, "w") as f:
                    json.dump(config,f,indent=4)
            elif response.status_code == 500:
                time.sleep(5)
                response = requests.post(url=murl, json=json.dumps(payload), headers=headers, verify=False)
                print(f"Second run\ncode: {response.status_code}\nresponse: {response.text}")
            else:
                print(f"Firmware creation failed\ncode:{response.status_code}\nbody{response.text}")
    except Exception as e:
        print(e)

'''
GET ALL FIRMWARES V1,V2
'''

def deploy_get_all_firmwaresv1():

    with open(config_file_path) as f:
        config = json.load(f)
    data = config["deploy_firmwares"]
    response,logger = firmwares_v1(req_dir_path,"deploy_get_firmwares_v1")
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

def deploy_get_all_firmwaresv2():

    with open(config_file_path) as f:
        config = json.load(f)
    data = config["deploy_firmwares"]
    response,logger = firmwares_v2(req_dir_path,"deploy_get_firmwares_v2")
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
GET FIRMWARE INFO V1,V2
'''
def deploy_get_firmware_info_v1():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_deploy_firmware_info_v1.txt")
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
            firmware = config["deploy_firmwares"][key]
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
                if firmware in result["Response Body"]:
                    print(f"{firmware} present in response")
                    logger.info(f"{firmware} present in response")
                else:
                    print(f"{firmware} not present in response")
                    logger.error(f"{firmware} not present in response")
            else:
                print(f"Failed response received")
                print(result["Response Body"])
                logger.error(f"Error Code: {result['Status Code']}")
                logger.error(f"Response Body: {result['Response Body']}")
    except Exception as e:
        print(f"Exception occurred while request action: {e}")
    finally:
        print("Test completed for get firmware info v1")

def deploy_get_firmware_info_v2():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_deploy_firmware_info_v2.txt")
    logger = setup_log(log_file, logger_name="file7")

    logger.info("Test initiated for get firmware info v2")
    with open(config_file_path,"r") as f:
        config = json.load(f)

    devices = config["test_devices"]
    try:
        for key,value in devices.items():
            firmware = config["deploy_firmwares"][key]
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
                if firmware in result["Response Body"]:
                    print(f"{firmware} present in response")
                    logger.info(f"{firmware} present in response")
                else:
                    print(f"{firmware} not present in response")
                    logger.error(f"{firmware} not present in response")

            else:
                print(f"Failed response received")
                print(result["Response Body"])
                logger.error(f"Error Code: {result['Status Code']}")
                logger.error(f"Response Body: {result['Response Body']}")
    except Exception as e:
        print(f"Exception occurred while request action: {e}")
    finally:
        print("Test completed for get firmware info v2")

#deploy_create_firmware()
#deploy_get_all_firmwaresv1()
#deploy_get_all_firmwaresv2()
#deploy_get_firmware_info_v1()
#deploy_get_firmware_info_v2()
