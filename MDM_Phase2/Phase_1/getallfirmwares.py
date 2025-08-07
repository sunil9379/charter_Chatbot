import random
from dotenv import load_dotenv
import os
import datetime
import requests
import json
from Phase_1.log_setup import setup_log
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")



def firmwares_v1(req_dir_path,log_name):
    #'''
    # set up log file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_{log_name}.txt")
    logger = setup_log(log_file, logger_name="file5")
    #'''
    print("Test initiated for get all firmwares v1")
    logger.info("Test initiated for get all firmwares v1")

    with open(config_file_path,"r") as f:
        config = json.load(f)
    url = config["url"]
    token = config["token"]
    payload = config["post_firmware"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    vendors = {
        "ata": "Ubee",
        "mta": "Technicolor",
        "cwl": "Motorola",
        "onu": "ALCATEL",
        "snu": "Humax"
    }
    result = {}
    try:
        
        for m in config['models_v2']:
            vendor_name = vendors.get(m)
            model_name = config["test_devices"][m]

            murl = f"{url}v1/catalog/vendors/{vendor_name}/models/{model_name}/firmwares"
            resp = requests.get(murl, headers=headers, verify=False)

            logger.info(f"Response for {model_name} device")
            if resp.status_code == 200:
                print(f"success\nCode: {resp.status_code}\nBody: {resp.text}")
                logger.info(f"Success response for {model_name} device")
                logger.info(f"Success Code: {resp.status_code}\nBody: {resp.text}")
                result[m] = resp.text
            else:
                print(f"Failure\nCode: {resp.status_code}\nBody: {resp.text}")
                logger.error(f"Failed to get response for {model_name} device")
                logger.error(f"Error Code: {resp.status_code}\nBody: {resp.text}")

    except Exception as e:
        print(e)

    return result,logger
#res=firmwares_v1()
#print(type(res))
#sample = "Test_snu001-P20-040625-25.5"
#if sample in res['snu']:
#    print("true")
#else:
#    print("false")

def firmwares_v2(req_dir_path,log_name):
    # set up log file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_{log_name}.txt")
    logger = setup_log(log_file, logger_name="file6")

    print("Test initiated for get all firmwares v2")
    logger.info("Test initiated for get all firmwares v2")

    with open(config_file_path, "r") as f:
        config = json.load(f)
    url = config["url"]
    token = config["token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    result = {}
    try:

        for m in config['models_v2']:
            model_name = config["test_devices"][m]
            ref_id = model_name + str(random.randint(1000,9999))
            murl = f"{url}v2/catalog/models/{model_name}/firmwares?referenceId={ref_id}"
            resp = requests.get(murl, headers=headers, verify=False)

            logger.info(f"Response for {model_name} device")
            if resp.status_code == 200:
                print(f"success\nCode: {resp.status_code}\nBody: {resp.text}")
                logger.info(f"Success response for {model_name} device")
                logger.info(f"Success Code: {resp.status_code}\nBody: {resp.text}")
                result[m] = resp.text
            else:
                print(f"Failure\nCode: {resp.status_code}\nBody: {resp.text}")
                logger.error(f"Failed to get response for {model_name} device")
                logger.error(f"Error Code: {resp.status_code}\nBody: {resp.text}")
    except Exception as e:
        print(e)

    return result,logger
#rest=firmwares_v2()
#fg = rest['ata']
#fg = json.loads(fg)
#rt=fg['eBbuFirmware']
#print(rt)
#sample = "Test_ata001-P20-040625-2025.5"
#if sample in rest['ata']:
#    print("true")
#else:
#    print("false")
'''    
gh = json.loads(rest["ata"])
jk = gh['firmwareVersions'][-1]
if sample in jk['firmwareVersion']:
    print("true")
else:
    print("false")
'''