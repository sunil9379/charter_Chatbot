import time
from Requests.import_device import device_import
from Requests.get_aggreagte_view import aggregate_view
from Requests.delete_firmware import firmware_delete
from Requests.getv2devices_byType import devices_bytype
from Requests.get_modelsType_v1 import devicev1_bytype
from Requests.get_device_defination import device_definition
from Requests.get_device_rules import device_rules
from Requests.excluded_devices_bytypes import excluded_devices
from Requests.publish_kafka import kafka_v1v2
from Requests.get_vendors_v1 import v1_vendors
from Requests.get_vendor_info import vendors_info
from Requests.getmodels_for_vendor import get_models_vendor
from Requests.get_approved_tag import v2_approved_tags
from Requests.create_approved_tags import create_approved_tags_v2
from Requests.delete_tags import delete_approved_tags
from Requests.backup import backup_list,backup_creation,download_backup

from Phase_1.Test_Stage.create_device import create_test_device
from Phase_1.Test_Stage.get_allmatched import test_get_allmatched
from Phase_1.Test_Stage.get_v2_devices import test_get_devices

from Phase_1.Certified_Stage.update_certify import update_device_certify
from Phase_1.Certified_Stage.get_matched_device import certify_matched_modelsv2
from Phase_1.Certified_Stage.get_modelsv2 import certify_get_call
from Phase_1.Certified_Stage.create_firmware import certify_create_firmware
from Phase_1.Certified_Stage.get_all_firmwares import certify_get_all_firmwaresv1,certify_get_all_firmwaresv2
from Phase_1.Certified_Stage.get_firmware_info import certify_get_firmware_info_v1,certify_get_firmware_info_v2
from Phase_1.Certified_Stage.put_firmware_versions import certify_put_firmware_version,put_get_firmware_info_v1,put_get_firmware_info_v2,put_get_all_firmwaresv1,put_get_all_firmwaresv2
from Phase_1.Certified_Stage.patch_firmware_decription import patch_firmware_description,patch_get_all_firmwares_v1,patch_get_all_firmwares_v2,patch_get_firmware_info_v1,patch_get_firmware_info_v2

from Phase_1.Deploy_Stage.update_deploy import device_deploy
from Phase_1.Deploy_Stage.get_all_matched import deploy_matched_modelsv2
from Phase_1.Deploy_Stage.get_modelsv2 import deploy_get_models
from Phase_1.Deploy_Stage.create_deploy_firmware import deploy_create_firmware,deploy_get_all_firmwaresv1,deploy_get_all_firmwaresv2,deploy_get_firmware_info_v1,deploy_get_firmware_info_v2
from Phase_1.Deploy_Stage.delete_flow import deploy_delete_flow

from Phase_1.Test_Stage.test_delete_flow import test_delete_flow
from Phase_1.Certified_Stage.certify_delete_flow import certified_delete_flow

def run_all():

    start = time.time()

    '''
    Test Stage
    '''

    #'''
    create_test_device()
    time.sleep(2)
    test_get_allmatched()
    time.sleep(2)
    test_get_devices()
    time.sleep(2)
    #'''

    '''
    Certify Stage
    '''

    #'''
    update_device_certify()
    time.sleep(2)
    certify_matched_modelsv2()
    certify_get_call()
    time.sleep(2)
    certify_create_firmware()
    time.sleep(2)
    certify_get_all_firmwaresv1()
    certify_get_all_firmwaresv2()
    time.sleep(2)
    certify_get_firmware_info_v1()
    certify_get_firmware_info_v2()
    time.sleep(2)
    certify_put_firmware_version()
    put_get_firmware_info_v1()
    put_get_firmware_info_v2()
    put_get_all_firmwaresv1()
    put_get_all_firmwaresv2()
    time.sleep(2)
    patch_firmware_description()
    patch_get_firmware_info_v1()
    patch_get_firmware_info_v2()
    patch_get_all_firmwares_v1()
    patch_get_all_firmwares_v2()
    #'''

    '''
    DEPLOY STAGE
    '''
    time.sleep(2)
    device_deploy()
    time.sleep(2)
    deploy_matched_modelsv2()
    time.sleep(2)
    deploy_get_models()
    time.sleep(2)
    deploy_create_firmware()
    deploy_get_all_firmwaresv1()
    deploy_get_all_firmwaresv2()
    deploy_get_firmware_info_v1()
    deploy_get_firmware_info_v2()
    time.sleep(2)
    deploy_delete_flow()
    time.sleep(5)

    #'''
    #DELETE FLOW FOR TEST STAGE
    create_test_device()
    time.sleep(2)
    test_delete_flow()
    time.sleep(5)

    #DELETE FLOW FOR CERTIFY STAGE
    create_test_device()
    time.sleep(2)
    update_device_certify()
    time.sleep(2)
    certify_create_firmware()
    time.sleep(2)
    certify_put_firmware_version()
    time.sleep(2)
    certified_delete_flow()
    time.sleep(5)
    #'''

    '''
    Phase 2
    '''

    '''
    device_import()
    time.sleep(1)
    aggregate_view()
    time.sleep(1)
    firmware_delete()
    time.sleep(1)
    devices_bytype()
    time.sleep(1)
    devicev1_bytype()
    time.sleep(1)
    device_definition()
    time.sleep(1)
    end = time.time()
    device_rules()
    time.sleep(1)
    excluded_devices()
    time.sleep(1)
    kafka_v1v2()
    time.sleep(1)
    v1_vendors()
    vendors_info()
    time.sleep(1)
    get_models_vendor()
    time.sleep(1)
    v2_approved_tags()
    time.sleep(1)
    create_approved_tags_v2()
    time.sleep(1)
    delete_approved_tags()
    time.sleep(1)
    backup_list()
    time.sleep(1)
    backup_creation()
    time.sleep(1)
    download_backup()
    time.sleep(1)
    '''

    end = time.time()

    total = end - start

    minutes = total / 60
    #print(f"Execution took {minutes:.2f} minutes (or {total:.2f} seconds)")
    if total <= 60:
        print(f"Execution time: {total: .2f} seconds")
    else:
        print(f"Execution time: {minutes: .2f} minutes")
