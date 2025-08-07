import json

from Phase_1.getallfirmwares import firmwares_v1,firmwares_v2
import os
import datetime
from Phase_1.log_setup import setup_log
from dotenv import load_dotenv
load_dotenv()

req_dir_path  =os.environ.get("P1_CERTIFY_LOG_PATH")
config_file_path = os.environ.get("P1_CONFIG_PATH")


def certify_get_all_firmwaresv1():

    with open(config_file_path) as f:
        config = json.load(f)
    data = config["certify_firmwares"]
    response,logger = firmwares_v1(req_dir_path,"get_firmwares_v1")
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

def certify_get_all_firmwaresv2():

    with open(config_file_path) as f:
        config = json.load(f)
    data = config["certify_firmwares"]
    response,logger = firmwares_v2(req_dir_path,"get_firmwares_v2")
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

#certify_get_all_firmwaresv1()
#certify_get_all_firmwaresv2()