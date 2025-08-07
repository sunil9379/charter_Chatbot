import copy
import random
import time

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_firmware():
    print("Test initiated for creating firmware")

    with open("config.json","r") as f:
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

            firmwareversion = f"{devices}-P20-040625-2025.5"
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
            print(murl)
            time.sleep(3)
            response = requests.post(url=murl, json=payload, headers=headers,verify=False)

            if response.status_code == 201:
                print("Firmware created successfully")
                print(time.sleep(2))
            elif response.status_code == 500:
                time.sleep(5)
                response = requests.post(url=murl, json=json.dumps(payload), headers=headers, verify=False)
                print(f"Second run\ncode: {response.status_code}\nresponse: {response.text}")
            else:
                print(f"Firmware creation failed\ncode:{response.status_code}\nbody{response.text}")
    except Exception as e:
        print(e)
create_firmware()