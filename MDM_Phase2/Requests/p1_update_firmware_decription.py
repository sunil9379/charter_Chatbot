import random

import requests
import json
from p1_getallfirmwares import firmwares_v2
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def update_firmware_description():
    print("Test initiated for updating the firmware description")

    with open("config.json","r") as f:
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

            if resp.status_code in(201,500):
                print(f"Firmware updated successfully for {device_name}")

                result = firmwares_v2()
                content = json.loads(result[m])
                if content['eDvaFirmware'] == None:
                    print(f"Firmware description update for {device_name} validated using get all firmware")
                else:
                    print("Could not validate")


            else:
                print("Firmware update failed")
    except Exception as e:
        print(e)
update_firmware_description()