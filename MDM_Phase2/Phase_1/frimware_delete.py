import os
import datetime
import json
import requests
import random
from Phase_1.log_setup import setup_log
from dotenv import load_dotenv

load_dotenv()
config_file_path = os.environ.get("P1_CONFIG_PATH")

def delete_firmware(req_dir_path,log_name,stage,call=None):

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{timestamp}_{log_name}.txt")
    logger = setup_log(log_file, logger_name="file1")

    print("Test initiated for Delete Firmware")
    logger.info("Test initiated for Delete Firmware")

    with open(config_file_path, "r") as f:
        config = json.load(f)

    if stage=="deploy":
        key="deploy_firmwares"
    if stage=="certify":
        key="updated_certify_firmwares"
    firmware_payload = config[key]
    devices = config["test_devices"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['token']}"
    }

    try:

        for key ,value in firmware_payload.items():
            model_name = devices[key]
            firmware = value
            ref_id = f"{model_name}" + str(random.randint(1000 ,9999))

            url = f"{config['url']}v2/catalog/models/{model_name}/firmwares/{firmware}?referenceId={ref_id}&userId=P3289462"
            print(f"Firmware deletion initiated for {model_name}")
            response = requests.delete(url=url, headers=headers, verify=False)

            if call=="call2":
                logger.info("Delete firmware initiated for second time")
                if response.status_code == 404:
                    print(f"Response code: {response.status_code}\nResponse body: {response.text}")
                    logger.info(f"Received Required response. Firmware {firmware} could not be found")
                    logger.info(f"Response code: {response.status_code}\nResponse body: {response.text}")

                else:
                    print(f"Response code: {response.status_code}\nResponse body: {response.text}")
                    logger.error(f"Error in deleting the firmware {firmware}")
                    logger.error(f"Response code: {response.status_code}\nResponse body: {response.text}")
            else:
                if response.status_code == 204:
                    print(f"Response code: {response.status_code}\nResponse body: {response.text}")
                    logger.info(f"Firmware {firmware} Successfully deleted")
                    logger.info(f"Response code: {response.status_code}\nResponse body: {response.text}")

                else:
                    print(f"Response code: {response.status_code}\nResponse body: {response.text}")
                    logger.error(f"Error in deleting the firmware {firmware}")
                    logger.error(f"Response code: {response.status_code}\nResponse body: {response.text}")



    except Exception as e:
        print(f"Exception while request action: {e}")
        logger.error(f"Exception while request action: {e}")

    finally:
        print("Test completed for deleting the firmware")
        logger.info("Test completed for deleting the firmware")
