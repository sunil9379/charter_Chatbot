from deepdiff import DeepDiff
import json
file1 = {
  "bootInfo": {
    "mac": "a4:cf:d2:f6:22:f8",
    "receivedTimestamp": 1753268614,
    "eventSource": "dpe01-int-r810.ise.charterlab.com"
  },
  "deviceLeaseInfo": {
    "action": "UPSERT",
    "timestamp": 1753268614,
    "macId": "a4:cf:d2:f6:22:f8",
    "networkProtocol": "IPv4",
    "deviceId": "ff:d2:f6:22:f8:00:03:00:01:a4:cf:d2:f6:22:f8",
    "ipAddress": "10.1.6.133",
    "cmMac": "a4:cf:d2:f6:22:f8",
    "regionId": "dhc01-int.ise.charterlab.com",
    "deviceType": "cm",
    "gatewayIp": "10.1.0.5",
    "eDeviceType": "ECM",
    "embeddedComponents": [
      "ECM:EDVA"
    ],
    "serialNumber": "M2C8A43008240",
    "hardwareVersion": "2.76.2",
    "currentFirmwareVersion": "EU2251-UNI-05.02.01-C3R",
    "requiredFirmwareVersion": "EU2251-UNI-05.02.01-C3R",
    "bootromVersion": "2.7.0alpha4",
    "model": "EU2251",
    "vendor": "Ubee",
    "vendorOui": "36:34:37:43:33:34",
    "legacyFootprint": "L-CHTR",
    "provisioningGroup": "devint",
    "classOfService": "",
    "dhcpCriteria": ""
  },
  "deviceCapabilities": {
    "certifiedSpeed": {
      "resiUpload": 1100000000,
      "smbUpload": 1100000000,
      "resiDownload": 2000000000,
      "smbDownload": 2000000000
    }
  }
}
file2 = {
  "bootInfo": {
    "receivedTimestamp": 1753268614,
    "eventSource": "dpe01-int-r810.ise.charterlab.com",
    "mac": "A4:CF:D2:F6:22:F8"
  },
  "deviceCapabilities": {
    "certifiedSpeed": {
      "smbUpload": 1100000000,
      "resiUpload": 1100000000,
      "smbDownload": 2000000000,
      "resiDownload": 2000000000
    }
  },
  "dlpqsDhcpLease": {
    "cmMac": "A4:CF:D2:F6:22:F8",
    "deviceType": "cm",
    "serialNumber": "M2C8A43008240",
    "macId": "A4:CF:D2:F6:22:F8",
    "ipAddress": "10.1.6.133",
    "legacyFootprint": "L-CHTR",
    "eDeviceType": "ECM",
    "gatewayIp": "10.1.0.5",
    "currentFirmwareVersion": "EU2251-UNI-05.02.01-C3R",
    "deviceId": "ff:d2:f6:22:f8:00:03:00:01:a4:cf:d2:f6:22:f8",
    "embeddedComponents": [
      "ECM:EDVA"
    ],
    "regionId": "dhc01-int.ise.charterlab.com",
    "vendor": "Ubee",
    "bootromVersion": "2.7.0alpha4",
    "provisioningGroup": "devint",
    "action": "UPSERT",
    "hardwareVersion": "2.76.2",
    "model": "EU2251",
    "networkProtocol": "IPv4",
    "requiredFirmwareVersion": "EU2251-UNI-05.02.01-C3R",
    "vendorOui": "36:34:37:43:33:34",
    "timestamp": 1753268614
  }
}

result = DeepDiff(file1,file2)
print(result)

