import random

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def update_firmware_version():

    print("Test initiated for update firmwares v1")

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

            payload = config["post_firmware"]
            model_name = config["test_devices"][m]
            firmware_version =f"{model_name}-P20-040625-2025.5"
            firmwaretp = "HTTPS"
            ref_id = model_name + str(random.randint(1000, 9999))
            ext_id = model_name + str(random.randint(1000, 9999))

            payload["firmwareVersion"] = f"{model_name}-P20-040625-2025.6"
            payload["firmwareFilename"] = payload['firmwareVersion']+".charter"
            payload["firmwareTransferProtocol"] = firmwaretp
            payload["metadata"]["referenceId"] = ref_id
            payload["metadata"]["externalId"] = ext_id

            murl = f"{url}v2/catalog/models/{model_name}/firmwares/{firmware_version}"
            print("payload: ",payload)
            resp = requests.put(url=murl,json=payload,headers=headers,verify=False)

            if resp.status_code == 201:
                print(f"Firmware {firmware_version} updated successfully\nstatus code: {resp.status_code}\nresponse: {resp.text}")
            else:
                print(f"Firmware {firmware_version} update failed\nstatus code: {resp.status_code}\nresponse: {resp.text}")

    except Exception as e:
        print(e)
    finally:
        print("Test completed to update firmware version")

    return
update_firmware_version()

with open("device_certify.json","r") as f:
    content = f.read()
print(type(content))
if "Test_ata001-P20-040625-2025.6" in content:
    print("Firmware updated successfully")
else:
    print("Firmware update failed")