import json

from p1_getfirmwareinfo import get_firmware_infov1,get_firmware_infov2


def get_firmware_ifo():
    with open("config.json","r") as f:
        config = json.load(f)
    url = config["url"]
    token = config["token"]
    devices = config["test_devices"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    firmwares = ["Test_ata001-P20-040625-2025.1","Test_mta001-P20-040625-2025.1","Test_cwl001-P20-040625-2025.1","Test_onu001-P20-040625-2025.1","Test_snu001-P20-040625-2025.1"]
    for m in config['models_v2']:
        d = devices[m]
        for f in firmwares:
            res = get_firmware_infov1(modelname=d,firmware=f)
            print(res)

get_firmware_ifo()
