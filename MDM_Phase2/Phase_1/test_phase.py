import json
import copy
import random
from dotenv import load_dotenv
import os
import datetime
from Phase_1.log_setup import setup_log
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("P1_TEST_LOG_PATH")  # this is Requests directory path
payload_test = os.environ.get("P1_TEST_PAYLOAD")

# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_create_test_devices.txt")
logger = setup_log(log_file, logger_name="file0")

def device_test():

    logger.info("-------------------------------**----------------------------")
    print("Test initiated to create device in test stage")
    logger.info("Test initiated to create device in test stage")

    #importing the payload and config file:
    try:
        print("importing the payload file")

        with open("test.json","r") as f:
            data = json.load(f)
            payload = copy.deepcopy(data)

        with open(config_file_path,"r") as f:
            content = json.load(f)
            url = content['url']
            token = content.get('token')
        logger.info("Imported the payload and config file")

    except Exception as e:
        logger.error(f"Failed to import the json files: {e}")
        print(f"Exception while importing payload/config: {e}")

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



    for key,value in vendors.items():
            print("inside for")
            data_model = payload

            if key=="ata":
               del data_model["modelDesc"]["deviceType"]
            else:
                data_model=data
            num = str(random.randint(100,999))
            data_model["modelName"] = f"Test_{key}" + num
            data_model["vendorName"] = value
            data_model["modelDesc"]["deviceTypeName"] = key
            url_m = url + "v2/catalog/models"
            ref_id = str(random.randint(1000,9999))
            ext_id = str(random.randint(1000,9999))

            data_model['metadata']['referenceId'] = ref_id
            data_model['metadata']['externalId'] = ext_id
            print(data_model)

            response = requests.post(url=url_m, headers = headers, json=data_model, verify=False)
            print("Response code: ",response.status_code)
            print("Response body: ",response.text)

            logger.info("======================================================")

            if response.status_code == 201:
                print("Device created in test stage successfully")
                logger.info(f"Device created for {key} in test stage successfully\nResponse Body: {response.text}")

                #content['test_devices'][m] = model_name
                #with open(config_file_path,"w") as f:
                #    json.dump(content,f, indent=4)

            else:
                print("Device creation in test stage failed")
                logger.error(f"Failed to create {key} device in test stage\nResponse Body: {response.text}")

    '''
    except Exception as e:
        print(f"Exception occurred in request action: {e}")
        logger.error(f"Exception occurred in request action: {e}")

    finally:
        print("Test completed for test stage")
        logger.info("Test completed for test stage")
    '''

device_test()