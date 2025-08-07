from Phase_1.getfirmwareinfo import get_firmware_infov1,get_firmware_infov2
import os
import datetime
import json
from Phase_1.log_setup import setup_log
from dotenv import load_dotenv

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")
req_dir_path = os.environ.get("P1_CERTIFY_LOG_PATH")


def certify_get_firmware_info_v1():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_firmware_info_v1.txt")
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
            firmware = config["certify_firmwares"][key]
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

def certify_get_firmware_info_v2():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_firmware_info_v2.txt")
    logger = setup_log(log_file, logger_name="file7")

    logger.info("Test initiated for get firmware info v2")
    with open(config_file_path,"r") as f:
        config = json.load(f)

    devices = config["test_devices"]
    try:
        for key,value in devices.items():
            firmware = config["certify_firmwares"][key]
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

#certify_get_firmware_info_v1()
#certify_get_firmware_info_v2()