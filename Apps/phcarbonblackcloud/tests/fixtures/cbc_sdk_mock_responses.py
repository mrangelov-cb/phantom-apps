"""Mocks for CBC Responses"""

import pytest


@pytest.fixture(scope="function")
def get_no_alert_response():
    return {
        "results": [],
        "num_found": 0,
    }


@pytest.fixture(scope="function")
def get_one_alert_response():
    return {
        "num_found": 1,
        "num_available": 1,
        "results": [
            {
                "id": "038894832709076d63111e99466f73575fcf3ca",
                "legacy_alert_id": "1DDU8H9N",
                "type": "CB_ANALYTICS",
                "org_key": "ABCD1234",
                "create_time": "2019-09-13T14:17:21.668Z",
                "last_update_time": "2019-09-13T14:17:21.668Z",
                "first_event_time": "2019-09-13T14:16:55.878Z",
                "last_event_time": "2019-09-13T14:16:55.878Z",
                "threat_id": "b7ce4f79e8903c09d2cd6b615c965c9f",
                "severity": 3,
                "category": "MONITORED",
                "device_id": 388948,
                "device_os": "MAC",
                "device_os_version": "10.14.6",
                "device_name": "some-system",
                "device_username": "support@carbonblack.com",
                "policy_id": 1,
                "policy_name": "default",
                "target_value": "MISSION_CRITICAL",
                "reason": "test",
                "reason_code": "123",
            }
        ],
    }


@pytest.fixture(scope="function")
def get_three_alerts_response():
    return {
        "num_found": 3,
        "num_available": 3,
        "results": [
            {
                "id": "038894832709076d63111e99466f73575fcf3ca",
                "legacy_alert_id": "1DDU8H9N",
                "type": "CB_ANALYTICS",
                "org_key": "ABCD1234",
                "create_time": "2019-09-13T14:17:21.668Z",
                "last_update_time": "2019-09-13T14:17:21.668Z",
                "first_event_time": "2019-09-13T14:16:55.878Z",
                "last_event_time": "2019-09-13T14:16:55.878Z",
                "threat_id": "b7ce4f79e8903c09d2cd6b615c965c9f",
                "severity": 3,
                "category": "MONITORED",
                "device_id": 388948,
                "device_os": "MAC",
                "device_os_version": "10.14.6",
                "device_name": "some-system",
                "device_username": "support@carbonblack.com",
                "policy_id": 1,
                "policy_name": "default",
                "target_value": "MISSION_CRITICAL",
                "reason": "test",
            },
            {
                "id": "038894832709076d63111e99466f73575fcf3sa",
                "legacy_alert_id": "1DDU8H9N",
                "type": "CB_ANALYTICS",
                "org_key": "ABCD1234",
                "create_time": "2019-09-13T14:17:21.668Z",
                "last_update_time": "2019-09-13T14:17:21.668Z",
                "first_event_time": "2019-09-13T14:16:55.878Z",
                "last_event_time": "2019-09-13T14:16:55.878Z",
                "threat_id": "b7ce4f79e8903c09d2cd6b615c965c9f",
                "severity": 6,
                "category": "MONITORED",
                "device_id": 388948,
                "device_os": "MAC",
                "device_os_version": "10.14.6",
                "device_name": "some-system",
                "device_username": "support@carbonblack.com",
                "policy_id": 1,
                "policy_name": "default",
                "target_value": "MISSION_CRITICAL",
                "reason_code": "123",
                "process_name": "someprocess.exe",
            },
            {
                "id": "038894832709076d63111e99466f73575fcf3cd",
                "legacy_alert_id": "1DDU8H9N",
                "type": "CB_ANALYTICS",
                "org_key": "ABCD1234",
                "create_time": "2019-09-13T14:17:21.668Z",
                "last_update_time": "2019-09-13T14:17:21.668Z",
                "first_event_time": "2019-09-13T14:16:55.878Z",
                "last_event_time": "2019-09-13T14:16:55.878Z",
                "threat_id": "b7ce4f79e8903c09d2cd6b615c965c9f",
                "severity": 9,
                "category": "MONITORED",
                "device_id": 388948,
                "device_os": "MAC",
                "device_os_version": "10.14.6",
                "device_name": "some-system",
                "device_username": "support@carbonblack.com",
                "policy_id": 1,
                "policy_name": "default",
                "target_value": "MISSION_CRITICAL",
            },
        ],
    }


@pytest.fixture(scope="function")
def get_one_alert_response():
    return {
        "num_found": 1,
        "num_available": 1,
        "results": [
            {
                "id": "038894832709076d63111e99466f73575fcf3ca",
                "legacy_alert_id": "1DDU8H9N",
                "type": "CB_ANALYTICS",
                "org_key": "ABCD1234",
                "create_time": "2019-09-13T14:17:21.668Z",
                "last_update_time": "2019-09-13T14:17:21.668Z",
                "first_event_time": "2019-09-13T14:16:55.878Z",
                "last_event_time": "2019-09-13T14:16:55.878Z",
                "threat_id": "b7ce4f79e8903c09d2cd6b615c965c9f",
                "severity": 3,
                "category": "MONITORED",
                "device_id": 388948,
                "device_os": "MAC",
                "device_os_version": "10.14.6",
                "device_name": "some-system",
                "device_username": "support@carbonblack.com",
                "policy_id": 1,
                "policy_name": "default",
                "target_value": "MISSION_CRITICAL",
            }
        ],
    }


@pytest.fixture(scope="function")
def return_single_alert_object():
    alert = {
        "id": "27a278d2150911eb86f1011a55e73b72",
        "org_key": "test",
        "threat_id": "B0RG",
        "workflow": {"state": "OPEN"},
        "last_update_time": "2020-03-13",
        "create_time": "2020-03-13",
    }
    return alert


@pytest.fixture(scope="function")
def get_10k1_alert_response(return_single_alert_object):
    return {
        "results": [return_single_alert_object for _ in range(0, 10000)],
        "num_found": 10001,
    }


@pytest.fixture(scope="function")
def get_binary_object():
    return {
        "sha256": "8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759",
        "architecture": ["amd64"],
        "available_file_size": 239440,
        "charset_id": 1200,
        "comments": None,
        "company_name": "Microsoft Corporation",
        "copyright": "© Microsoft Corporation. All rights reserved.",
        "file_available": True,
        "file_description": "Windows Modules Installer Worker",
        "file_size": 239440,
        "file_version": "10.0.19041.860 (WinBuild.160101.0800)",
        "internal_name": "TiWorker.exe",
        "lang_id": 1033,
        "md5": "b571fd1c411406d9c55c790073777633",
        "original_filename": "TiWorker.exe",
        "os_type": "WINDOWS",
        "private_build": None,
        "product_description": None,
        "product_name": "Microsoft® Windows® Operating System",
        "product_version": "10.0.19041.860",
        "special_build": None,
        "trademark": None,
    }


@pytest.fixture(scope="function")
def get_reputation_override_sha256_object():
    return {
        "id": "e9410b754ea011ebbfd0db2585a41b07",
        "created_by": "example@example.com",
        "create_time": "2021-01-04T15:24:18.002Z",
        "description": "An override for a foo.exe",
        "override_list": "BLACK_LIST",
        "override_type": "SHA256",
        "sha256_hash": "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a",
        "filename": "TiWorker.exe",
    }


@pytest.fixture(scope="function")
def get_reputation_override_sha256_search_single_response(
    get_reputation_override_sha256_object,
):
    return {
        "num_found": 1,
        "results": [get_reputation_override_sha256_object],
    }


@pytest.fixture(scope="function")
def get_reputation_override_sha256_search_multiple_response(
    get_reputation_override_sha256_object,
):
    return {
        "num_found": 2,
        "results": [get_reputation_override_sha256_object for _ in range(0, 2)],
    }


@pytest.fixture(scope="function")
def get_reputation_override_sha256_search_no_response():
    return {
        "num_found": 0,
        "results": [],
    }


@pytest.fixture(scope="function")
def get_device_object():
    return {
        "activation_code": None,
        "activation_code_expiry_time": "2017-09-21T15:44:34.757Z",
        "ad_group_id": 1706,
        "appliance_name": None,
        "appliance_uuid": None,
        "av_ave_version": "8.3.62.126",
        "av_engine": "4.13.0.207-ave.8.3.62.126:avpack.8.5.0.92:vdf.8.18.22.172",
        "av_last_scan_time": None,
        "av_master": False,
        "av_pack_version": "8.5.0.92",
        "av_product_version": "4.13.0.207",
        "av_status": ["AV_DEREGISTERED"],
        "av_update_servers": None,
        "av_vdf_version": "8.18.22.172",
        "cluster_name": None,
        "current_sensor_policy_name": "default",
        "datacenter_name": None,
        "deployment_type": "WORKLOAD",
        "deregistered_time": "2021-01-28T12:44:25.553Z",
        "device_meta_data_item_list": [
            {"key_name": "SUBNET", "key_value": "10.126.6", "position": 0},
            {"key_name": "OS_MAJOR_VERSION", "key_value": "Windows 10", "position": 0},
        ],
        "device_owner_id": 70963,
        "email": "Administrator",
        "esx_host_name": None,
        "esx_host_uuid": None,
        "first_name": None,
        "id": 354648,
        "last_contact_time": "2021-01-28T12:43:26.243Z",
        "last_device_policy_changed_time": None,
        "last_device_policy_requested_time": "2021-01-26T17:44:53.274Z",
        "last_external_ip_address": "66.170.99.2",
        "last_internal_ip_address": "10.126.6.201",
        "last_location": "OFFSITE",
        "last_name": None,
        "last_policy_updated_time": "2020-10-22T20:47:17.097Z",
        "last_reported_time": "2021-01-28T19:59:41.537Z",
        "last_reset_time": None,
        "last_shutdown_time": None,
        "linux_kernel_version": None,
        "login_user_name": "WIN-2016-BM\\Administrator",
        "mac_address": "000000000000",
        "middle_name": None,
        "name": "WIN-2016-BM",
        "organization_id": 428,
        "organization_name": "cb-internal-partnersolutions.org",
        "os": "WINDOWS",
        "os_version": "Windows Server 2019 x64",
        "passive_mode": False,
        "policy_id": 2198,
        "policy_name": "default",
        "policy_override": False,
        "quarantined": False,
        "registered_time": "2021-01-26T16:58:56.346Z",
        "scan_last_action_time": None,
        "scan_last_complete_time": None,
        "scan_status": None,
        "sensor_kit_type": "WINDOWS",
        "sensor_out_of_date": False,
        "sensor_pending_update": False,
        "sensor_states": [
            "ACTIVE",
            "LIVE_RESPONSE_NOT_RUNNING",
            "LIVE_RESPONSE_NOT_KILLED",
            "LIVE_RESPONSE_ENABLED",
        ],
        "sensor_version": "3.7.0.503",
        "status": "DEREGISTERED",
        "target_priority": "MEDIUM",
        "uninstall_code": "6EAAJU4R",
        "vcenter_host_url": None,
        "vcenter_name": None,
        "vcenter_uuid": None,
        "vdi_base_device": None,
        "virtual_machine": True,
        "virtualization_provider": "VMW_ESX",
        "vm_ip": None,
        "vm_name": None,
        "vm_uuid": None,
        "vulnerability_score": 0.0,
        "vulnerability_severity": None,
        "windows_platform": None,
    }


@pytest.fixture(scope="function")
def get_quarantined_device_object():
    return {
        "activation_code": None,
        "activation_code_expiry_time": "2017-09-21T15:44:34.757Z",
        "ad_group_id": 1706,
        "appliance_name": None,
        "appliance_uuid": None,
        "av_ave_version": "8.3.62.126",
        "av_engine": "4.13.0.207-ave.8.3.62.126:avpack.8.5.0.92:vdf.8.18.22.172",
        "av_last_scan_time": None,
        "av_master": False,
        "av_pack_version": "8.5.0.92",
        "av_product_version": "4.13.0.207",
        "av_status": ["AV_DEREGISTERED"],
        "av_update_servers": None,
        "av_vdf_version": "8.18.22.172",
        "cluster_name": None,
        "current_sensor_policy_name": "default",
        "datacenter_name": None,
        "deployment_type": "WORKLOAD",
        "deregistered_time": "2021-01-28T12:44:25.553Z",
        "device_meta_data_item_list": [
            {"key_name": "SUBNET", "key_value": "10.126.6", "position": 0},
            {"key_name": "OS_MAJOR_VERSION", "key_value": "Windows 10", "position": 0},
        ],
        "device_owner_id": 70963,
        "email": "Administrator",
        "esx_host_name": None,
        "esx_host_uuid": None,
        "first_name": None,
        "id": 354648,
        "last_contact_time": "2021-01-28T12:43:26.243Z",
        "last_device_policy_changed_time": None,
        "last_device_policy_requested_time": "2021-01-26T17:44:53.274Z",
        "last_external_ip_address": "66.170.99.2",
        "last_internal_ip_address": "10.126.6.201",
        "last_location": "OFFSITE",
        "last_name": None,
        "last_policy_updated_time": "2020-10-22T20:47:17.097Z",
        "last_reported_time": "2021-01-28T19:59:41.537Z",
        "last_reset_time": None,
        "last_shutdown_time": None,
        "linux_kernel_version": None,
        "login_user_name": "WIN-2016-BM\\Administrator",
        "mac_address": "000000000000",
        "middle_name": None,
        "name": "WIN-2016-BM",
        "organization_id": 428,
        "organization_name": "cb-internal-partnersolutions.org",
        "os": "WINDOWS",
        "os_version": "Windows Server 2019 x64",
        "passive_mode": False,
        "policy_id": 2198,
        "policy_name": "default",
        "policy_override": False,
        "quarantined": True,
        "registered_time": "2021-01-26T16:58:56.346Z",
        "scan_last_action_time": None,
        "scan_last_complete_time": None,
        "scan_status": None,
        "sensor_kit_type": "WINDOWS",
        "sensor_out_of_date": False,
        "sensor_pending_update": False,
        "sensor_states": [
            "ACTIVE",
            "LIVE_RESPONSE_NOT_RUNNING",
            "LIVE_RESPONSE_NOT_KILLED",
            "LIVE_RESPONSE_ENABLED",
        ],
        "sensor_version": "3.7.0.503",
        "status": "DEREGISTERED",
        "target_priority": "MEDIUM",
        "uninstall_code": "6EAAJU4R",
        "vcenter_host_url": None,
        "vcenter_name": None,
        "vcenter_uuid": None,
        "vdi_base_device": None,
        "virtual_machine": True,
        "virtualization_provider": "VMW_ESX",
        "vm_ip": None,
        "vm_name": None,
        "vm_uuid": None,
        "vulnerability_score": 0.0,
        "vulnerability_severity": None,
        "windows_platform": None,
    }


@pytest.fixture(scope="function")
def get_report_no_iocs_response():
    return {
        "results": [
            {
                "id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
                "timestamp": 1592578548,
                "title": "simple hash - chrome.exe",
                "description": "A regular non-malicious hash to test watchlist event triggering",
                "severity": 1,
                "link": None,
                "tags": None,
                "iocs": None,
                "iocs_v2": [],
                "visibility": None,
            }
        ]
    }


@pytest.fixture(scope="function")
def get_report_object():
    return {
        "id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "timestamp": 1592578548,
        "title": "simple hash - chrome.exe",
        "description": "A regular non-malicious hash to test watchlist event triggering",
        "severity": 1,
        "link": None,
        "tags": None,
        "iocs": None,
        "iocs_v2": [
            {
                "id": "test",
                "match_type": "equality",
                "field": "process_hash",
                "values": ["b2e5665591b2118ca13709f61b60d700"],
            }
        ],
        "visibility": None,
    }


@pytest.fixture(scope="function")
def get_report_with_one_ioc_response():
    return {
        "results": [
            {
                "id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
                "timestamp": 1592578548,
                "title": "simple hash - chrome.exe",
                "description": "A regular non-malicious hash to test watchlist event triggering",
                "severity": 1,
                "link": None,
                "tags": None,
                "iocs": None,
                "iocs_v2": [
                    {
                        "id": "test",
                        "match_type": "equality",
                        "field": "process_hash",
                        "values": ["b2e5665591b2118ca13709f61b60d700"],
                    }
                ],
                "visibility": None,
            }
        ]
    }


@pytest.fixture(scope="function")
def get_full_report_response():
    return {
        "results": [
            {
                "id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
                "timestamp": 1592578548,
                "title": "simple hash - chrome.exe",
                "description": "A regular non-malicious hash to test watchlist event triggering",
                "severity": 1,
                "link": None,
                "tags": None,
                "iocs": None,
                "iocs_v2": [
                    {
                        "id": i,
                        "match_type": "equality",
                        "field": "process_name",
                        "values": ["wicked.exe"],
                    }
                    for i in range(0, 1000)
                ],
                "visibility": None,
            }
        ]
    }


@pytest.fixture(scope="function")
def get_watchlist_object():
    return {
        "name": "ATT&CK Framework",
        "description": "Existing description for the watchlist.",
        "id": "TC09QSSTRHqRF2qAAli3TA",
        "tags_enabled": True,
        "alerts_enabled": False,
        "create_timestamp": 1597173159,
        "last_update_timestamp": 1597173159,
        "report_ids": [
            "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        ],
        "classifier": {"key": "feed_id", "value": "feed_id_associated"},
    }


@pytest.fixture(scope="function")
def get_session_init_object():
    return {
        "id": "1:2468",
        "device_id": 2468,
        "check_in_timeout": 900,
        "session_timeout": 900,
        "status": "PENDING",
        "current_command_index": 0,
        "create_time": "2021-04-07T17:49:58.792Z",
        "device_check_in_time": "2021-04-07T17:49:58.793Z",
    }


@pytest.fixture(scope="function")
def get_session_poll_object():
    return {
        "hostname": None,
        "address": None,
        "os_version": None,
        "current_working_directory": "C:\\Windows\\system32",
        "supported_commands": [
            "put file",
            "get file",
            "memdump",
            "create directory",
            "delete file",
            "directory list",
            "reg enum key",
            "reg query value",
            "reg create key",
            "reg delete key",
            "reg delete value",
            "reg set value",
            "process list",
            "kill",
            "create process",
        ],
        "drives": ["A:\\", "C:\\", "D:\\"],
        "id": "1:2468",
        "device_id": 2468,
        "check_in_timeout": 900,
        "session_timeout": 900,
        "sensor_check_in_time": 1502126744685,
        "status": "active",
        "current_command_index": 0,
        "create_time": 1502126655758,
    }


@pytest.fixture(scope="function")
def get_list_proc_start_object():
    return {
        "id": 10,
        "session_id": "1:2468",
        "device_id": 2468,
        "command_timeout": 120,
        "status": "pending",
        "name": "process list",
        "object": None,
        "completion_time": 0,
    }


@pytest.fixture(scope="function")
def get_list_proc_end_object():
    return {
        "id": 10,
        "session_id": "1:2468",
        "device_id": 2468,
        "command_timeout": 120,
        "status": "complete",
        "name": "process list",
        "object": None,
        "completion_time": 2345678901,
        "processes": [
            {
                "process_pid": 303,
                "create_time": 1476390670,
                "proc_guid": "6EDF43E9-11B3-469F-B80F-D7917D60CC62",
                "process_path": "proc1",
                "process_cmdline": "proc1",
                "sid": "S-1-4-888",
                "process_username": "root",
                "parent_pid": 1,
                "parent_guid": "D0A5F3CA-E08D-41CA-8FDF-BBF95850752F",
            },
            {
                "process_pid": 805,
                "create_time": 1476390670,
                "proc_guid": "17FD30A5-B8BF-41F9-8B38-4137B7241D4B",
                "process_path": "server",
                "process_cmdline": "server",
                "sid": "S-1-4-888",
                "process_username": "root",
                "parent_pid": 1,
                "parent_guid": "D0A5F3CA-E08D-41CA-8FDF-BBF95850752F",
            },
            {
                "process_pid": 1024,
                "create_time": 1476390670,
                "proc_guid": "5EC3FFCA-238C-496E-ADEA-DF4F9EC4F473",
                "process_path": "borg",
                "process_cmdline": "borg",
                "sid": "S-1-4-888",
                "process_username": "root",
                "parent_pid": 1,
                "parent_guid": "D0A5F3CA-E08D-41CA-8FDF-BBF95850752F",
            },
        ],
    }


@pytest.fixture(scope="function")
def get_file_resp_object():
    return {
        "status": "complete",
        "values": [],
        "file_details": {
            "offset": 0,
            "count": 1,
            "file_id": "bdbd44f3-b9c8-445f-9a7a-51a0541624e0",
        },
        "id": 10,
        "name": "get file",
        "result_code": 0,
        "result_desc": "",
        "sub_keys": [],
        "files": [],
        "input": {"name": "get file", "object": "test.txt"},
        "finish_time": "2021-10-27T08:14:00.352Z",
        "create_time": "2021-10-27T08:14:00Z",
    }


@pytest.fixture(scope="function")
def get_report_response():
    return {
        "id": "report_id",
        "timestamp": 1592578548,
        "title": "simple hash - chrome.exe",
        "description": "A regular non-malicious hash to test watchlist event triggering",
        "severity": 1,
        "link": None,
        "tags": None,
        "iocs": None,
        "iocs_v2": [
            {
                "id": "109027d2-064c-477d-aa34-528606ef72a1",
                "match_type": "equality",
                "values": ["b2e5665591b2118ca13709f61b60d700"],
                "field": "md5",
                "link": "https://www.yahoo.com",
            }
        ],
        "visibility": None,
    }


@pytest.fixture(scope="function")
def get_feed_build_response():
    return {
        "feedinfo": {
            "name": "test_feed",
            "provider_url": "http://example.com",
            "summary": "test_feed_sum information",
            "category": "test_feed_cat",
        },
        "reports": [],
    }


@pytest.fixture(scope="function")
def get_feed_retrieve_object():
    return {
        "feedinfo": {
            "name": "EA16489_test_5",
            "owner": "WNEXFKQ7",
            "provider_url": "http://example.com",
            "summary": "Simple IOC trigger",
            "category": "None",
            "source_label": None,
            "access": "private",
            "id": "123",
        },
        "reports": [
            {
                "id": "109027d1-064c-477d-aa34-528606ef72a9",
                "timestamp": 1592578548,
                "title": "simple hash - chrome.exe",
                "description": "A regular non-malicious hash to test watchlist event triggering",
                "severity": 1,
                "link": None,
                "tags": None,
                "iocs": None,
                "iocs_v2": [
                    {
                        "id": "109027d2-064c-477d-aa34-528606ef72a1",
                        "match_type": "equality",
                        "values": ["b2e5665591b2118ca13709f61b60d700"],
                        "field": "md5",
                    }
                ],
                "visibility": None,
            }
        ],
    }


@pytest.fixture(scope="function")
def get_watchlist_build_response():
    return {
        "name": "test_watchlist",
        "description": "test_watchlist",
        "tags_enabled": False,
        "alerts_enabled": True,
        "report_ids": ["123", "456", "789"],
    }


@pytest.fixture(scope="function")
def get_binary_file_response():
    return {
        "found": [
            {
                "sha256": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776",
                "url": "https://www.example.com/a/b/c",
            }
        ],
        "not_found": [],
        "error": [],
    }


@pytest.fixture(scope="function")
def get_binary_metadata_response():
    return {
        "sha256": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776",
        "architecture": ["amd64"],
        "available_file_size": 96672,
        "charset_id": 1200,
        "comments": None,
        "company_name": None,
        "copyright": "\u00a9 Microsoft Corporation. All rights reserved.",
        "file_available": True,
        "file_description": "Runtime Broker",
        "file_size": 96672,
        "file_version": "10.0.16299.15 (WinBuild.160101.0800)",
        "internal_name": "RuntimeBroker.exe",
        "lang_id": 1033,
        "md5": "bd4401441a21bf1abce6404f4231db4d",
        "original_filename": "RuntimeBroker.exe",
        "os_type": "WINDOWS",
        "private_build": None,
        "product_description": None,
        "product_name": "Microsoft\u00ae Windows\u00ae Operating System",
        "product_version": "10.0.16299.15",
        "special_build": None,
        "trademark": None,
    }


@pytest.fixture(scope="function")
def get_cb_analytics_alert():
    return {
        "type": "CB_ANALYTICS",
        "id": "86123310980efd0b38111eba4bfa5e98aa30b19",
        "legacy_alert_id": "62802DCE",
        "org_key": "4JDT3MX9Q",
        "create_time": "2021-05-13T00:20:46.474Z",
        "last_update_time": "2021-05-13T00:27:22.846Z",
        "first_event_time": "2021-05-13T00:20:13.043Z",
        "last_event_time": "2021-05-13T00:20:13.044Z",
        "threat_id": "a26842be6b54ea2f58848b23a3461as16",
        "severity": 1,
        "category": "MONITORED",
        "device_id": 8612331,
        "device_os": "WINDOWS",
        "device_os_version": "Windows Server 2019 x64",
        "device_name": "win-2016-devrel",
        "device_username": "Administrator",
        "policy_id": 7113786,
        "policy_name": "Standard",
        "target_value": "MEDIUM",
        "workflow": {
            "state": "OPEN",
            "remediation": "None",
            "last_update_time": "2021-05-13T00:20:46.474Z",
            "comment": "None",
            "changed_by": "Carbon Black",
        },
        "notes_present": False,
        "tags": "None",
        "reason": "A port scan was detected from 10.169.255.100 on an external network (off-prem).",
        "reason_code": "R_SCAN_OFF",
        "process_name": "svchost.exe",
        "device_location": "OFFSITE",
        "created_by_event_id": "0980efd0b38111eba4bfa5e98aa30b19",
        "threat_indicators": [
            {
                "process_name": "svchost.exe",
                "sha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                "ttps": [
                    "ACTIVE_SERVER",
                    "MITRE_T1046_NETWORK_SERVICE_SCANNING",
                    "NETWORK_ACCESS",
                    "PORTSCAN",
                ],
            }
        ],
        "threat_activity_dlp": "NOT_ATTEMPTED",
        "threat_activity_phish": "NOT_ATTEMPTED",
        "threat_activity_c2": "NOT_ATTEMPTED",
        "threat_cause_actor_sha256": "10.169.255.100",
        "threat_cause_actor_name": "svchost.exe -k RPCSS -p",
        "threat_cause_actor_process_pid": "868-132563418721238249-0",
        "threat_cause_process_guid": "4JDT3MX9Q-008369eb-00000364-00000000-1d6f5ba1b173ce9",
        "threat_cause_parent_guid": "None",
        "threat_cause_reputation": "ADAPTIVE_WHITE_LIST",
        "threat_cause_threat_category": "NEW_MALWARE",
        "threat_cause_vector": "UNKNOWN",
        "threat_cause_cause_event_id": "0980efd1b38111eba4bfa5e98aa30b19",
        "blocked_threat_category": "UNKNOWN",
        "not_blocked_threat_category": "NEW_MALWARE",
        "kill_chain_status": ["RECONNAISSANCE"],
        "sensor_action": "None",
        "run_state": "RAN",
        "policy_applied": "NOT_APPLIED",
    }


@pytest.fixture(scope="function")
def get_enriched_events_search_job_response():
    return {"job_id": "08ffa932-b633-4107-ba56-8741e929e48b"}


@pytest.fixture(scope="function")
def get_enriched_events_search_job_results_response():
    return {
        "contacted": 41,
        "completed": 41,
        "query": {
            "cb.event_docs": True,
            "cb.max_backend_timestamp": 1603973841000,
            "cb.min_backend_timestamp": 0,
            "cb.min_device_timestamp": 0,
            "cb.preview_results": 500,
            "cb.use_agg": True,
            "facet": False,
            "fq": '{!collapse field=event_id sort="device_timestamp desc"}',
            "q": "(process_pid:1000 OR process_pid:2000)",
            "rows": 500,
            "start": 0,
        },
        "search_initiated_time": 1603973841206,
        "connector_id": "P1PFUIAN32",
    }


@pytest.fixture(scope="function")
def get_enriched_events_search_job_events_response():
    return {
        "approximate_unaggregated": 2,
        "completed": 7,
        "contacted": 7,
        "num_aggregated": 2,
        "num_available": 2,
        "num_found": 2,
        "results": [
            {
                "alert_category": ["OBSERVED"],
                "alert_id": ["62802DCE"],
                "backend_timestamp": "2021-05-13T00:21:13.086Z",
                "device_external_ip": "66.170.99.2",
                "device_group_id": 0,
                "device_id": 8612331,
                "device_installed_by": "Administrator",
                "device_internal_ip": "10.169.255.100",
                "device_location": "OFFSITE",
                "device_name": "win-2016-devrel",
                "device_os": "WINDOWS",
                "device_os_version": "Windows Server 2019 x64",
                "device_policy": "standard",
                "device_policy_id": 7113786,
                "device_target_priority": "MEDIUM",
                "device_timestamp": "2021-05-13T00:20:13.044Z",
                "document_guid": "VNs_NgMIQ-u3_06Sa4Sclg",
                "enriched": True,
                "enriched_event_type": "NETWORK",
                "event_attack_stage": ["RECONNAISSANCE"],
                "event_description": 'The application "<share><link '
                'hash="7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6"'
                '-k RPCSS -p</link></share>" accepted a '
                "<accent>TCP/135</accent> connection from "
                "<share><accent>10.169.255.100</accent></share><accent>:38240</accent> "
                "to "
                "<share><accent>10.126.6.201</accent></share><accent>:135</accent>. "
                "The device was off the corporate network "
                "using the public address "
                "<accent>66.170.99.2</accent> "
                "(<accent>win-2016-devrel</accent>, located "
                "in San Jose CA, United States). The "
                "operation was successful.",
                "event_id": "0980efd1b38111eba4bfa5e98aa30b19",
                "event_network_inbound": True,
                "event_network_local_ipv4": "10.126.6.201",
                "event_network_protocol": "TCP",
                "event_network_remote_ipv4": "10.169.255.100",
                "event_network_remote_port": 38240,
                "event_report_code": "SUB_RPT_NONE",
                "event_threat_score": [1],
                "event_type": "netconn",
                "ingress_time": 1620865258371,
                "legacy": True,
                "netconn_inbound": True,
                "netconn_ipv4": 178913124,
                "netconn_local_ipv4": 176031433,
                "netconn_local_port": 135,
                "netconn_port": 135,
                "netconn_protocol": "PROTO_TCP",
                "org_id": "4JDT3MX9Q",
                "parent_effective_reputation": "LOCAL_WHITE",
                "parent_effective_reputation_source": "CERT",
                "parent_guid": "4JDT3MX9Q-008369eb-00000268-00000000-1d6f5ba1abcf6fc",
                "parent_hash": [
                    "e8ea65fb51db75b1cb93890bee4364fc0b804f8f68e1817887e4a7f767ceb9ab"
                ],
                "parent_name": "c:\\windows\\system32\\services.exe",
                "parent_pid": 616,
                "parent_reputation": "NOT_LISTED",
                "process_cmdline": [
                    "C:\\Windows\\system32\\svchost.exe -k RPCSS " "-p"
                ],
                "process_cmdline_length": [43],
                "process_effective_reputation": "LOCAL_WHITE",
                "process_effective_reputation_source": "CERT",
                "process_guid": "4JDT3MX9Q-008369eb-00000364-00000000-1d6f5ba1b173ce9",
                "process_hash": [
                    "8a0a29438052faed8a2532da50455756",
                    "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                ],
                "process_name": "c:\\windows\\system32\\svchost.exe",
                "process_pid": [868],
                "process_reputation": "ADAPTIVE_WHITE_LIST",
                "process_sha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                "process_start_time": "2021-01-28T13:12:17.823Z",
                "process_username": ["NT AUTHORITY\\NETWORK SERVICE"],
                "ttp": [
                    "PORTSCAN",
                    "MITRE_T1046_NETWORK_SERVICE_SCANNING",
                    "NETWORK_ACCESS",
                    "ACTIVE_SERVER",
                ],
            },
            {
                "alert_category": ["OBSERVED"],
                "alert_id": ["62802DCE"],
                "backend_timestamp": "2021-05-13T00:21:08.028Z",
                "device_external_ip": "66.170.99.2",
                "device_group_id": 0,
                "device_id": 8612331,
                "device_installed_by": "Administrator",
                "device_internal_ip": "10.169.255.100",
                "device_location": "OFFSITE",
                "device_name": "win-2016-devrel",
                "device_os": "WINDOWS",
                "device_os_version": "Windows Server 2019 x64",
                "device_policy": "standard",
                "device_policy_id": 7113786,
                "device_target_priority": "MEDIUM",
                "device_timestamp": "2021-05-13T00:20:13.043Z",
                "document_guid": "WwZPWPLITqSNpAmQKagBYw",
                "enriched": True,
                "enriched_event_type": "NETWORK",
                "event_attack_stage": ["RECONNAISSANCE"],
                "event_description": 'The application "<share><link '
                'hash="7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6"'
                '-k termsvcs -s TermService</link></share>" '
                "accepted a <accent>TCP/3389</accent> "
                "connection from "
                "<share><accent>10.169.255.100</accent></share><accent>:38604</accent> "
                "to "
                "<share><accent>10.126.6.201</accent></share><accent>:3389</accent>. "
                "The device was off the corporate network "
                "using the public address "
                "<accent>66.170.99.2</accent> "
                "(<accent>win-2016-devrel</accent>, located "
                "in San Jose CA, United States). The "
                "operation was successful.",
                "event_id": "0980efd0b38111eba4bfa5e98aa30b19",
                "event_network_inbound": True,
                "event_network_local_ipv4": "10.126.6.201",
                "event_network_protocol": "TCP",
                "event_network_remote_ipv4": "10.169.255.100",
                "event_network_remote_port": 38604,
                "event_report_code": "SUB_RPT_NONE",
                "event_threat_score": [1],
                "event_type": "netconn",
                "ingress_time": 1620865258370,
                "legacy": True,
                "netconn_inbound": True,
                "netconn_ipv4": 178913124,
                "netconn_local_ipv4": 176031433,
                "netconn_local_port": 3389,
                "netconn_port": 3389,
                "netconn_protocol": "PROTO_TCP",
                "org_id": "4JDT3MX9Q",
                "parent_effective_reputation": "LOCAL_WHITE",
                "parent_effective_reputation_source": "CERT",
                "parent_guid": "4JDT3MX9Q-008369eb-00000268-00000000-1d6f5ba1abcf6fc",
                "parent_hash": [
                    "e8ea65fb51db75b1cb93890bee4364fc0b804f8f68e1817887e4a7f767ceb9ab"
                ],
                "parent_name": "c:\\windows\\system32\\services.exe",
                "parent_pid": 616,
                "parent_reputation": "NOT_LISTED",
                "process_cmdline": [
                    "C:\\Windows\\System32\\svchost.exe -k " "termsvcs -s TermService"
                ],
                "process_cmdline_length": [58],
                "process_effective_reputation": "LOCAL_WHITE",
                "process_effective_reputation_source": "CERT",
                "process_guid": "4JDT3MX9Q-008369eb-0000016c-00000000-1d6f5ba1b4bd98d",
                "process_hash": [
                    "8a0a29438052faed8a2532da50455756",
                    "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                ],
                "process_name": "c:\\windows\\system32\\svchost.exe",
                "process_pid": [364],
                "process_reputation": "ADAPTIVE_WHITE_LIST",
                "process_sha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
                "process_start_time": "2021-01-28T13:12:18.168Z",
                "process_username": ["NT AUTHORITY\\NETWORK SERVICE"],
                "ttp": [
                    "PORTSCAN",
                    "MITRE_T1046_NETWORK_SERVICE_SCANNING",
                    "NETWORK_ACCESS",
                    "ACTIVE_SERVER",
                ],
            },
        ],
    }


@pytest.fixture(scope="function")
def get_execute_start_object():
    return {
        "status": "PENDING",
        "values": [],
        "process_details": {"pid": 0, "return_code": -1},
        "id": 15,
        "name": "create process",
        "result_code": 0,
        "result_desc": "",
        "sub_keys": [],
        "files": [],
        "input": {
            "wait": True,
            "name": "create process",
            "output_file": "C:\\demo\\output.txt",
            "object": "cmd.exe /c dir",
        },
        "create_time": "2021-10-29T13:47:07Z",
        "finish_time": "2021-10-29T13:47:07.732Z",
    }


@pytest.fixture(scope="function")
def get_execute_end_object():
    return {
        "status": "COMPLETE",
        "values": [],
        "process_details": {"pid": 3272, "return_code": 0},
        "id": 15,
        "name": "create process",
        "result_code": 0,
        "result_type": "WinHresult",
        "result_desc": "",
        "sub_keys": [],
        "files": [],
        "input": {
            "wait": True,
            "name": "create process",
            "output_file": "C:\\demo\\output.txt",
            "object": "cmd.exe /c dir",
        },
        "create_time": "2021-10-29T13:47:07Z",
        "finish_time": "2021-10-29T13:47:08Z",
    }


@pytest.fixture(scope="function")
def get_process_validation_resp():
    return {"valid": True, "value_search_query": False}


@pytest.fixture(scope="function")
def post_process_details_resp():
    return {"job_id": "ccc47a52-9a61-4c77-8652-8a03dc187b98"}


@pytest.fixture(scope="function")
def get_process_details_status_resp():
    return {"contacted": 16, "completed": 16}


@pytest.fixture(scope="function")
def get_process_details_resp():
    return {
        "contacted": 16,
        "completed": 16,
        "num_available": 1,
        "num_found": 1,
        "results": [
            {
                "backend_timestamp": "2020-08-28T19:14:40.394Z",
                "childproc_count": 333576,
                "crossproc_count": 0,
                "device_external_ip": "34.56.78.90",
                "device_group_id": 0,
                "device_id": 176678,
                "device_location": "UNKNOWN",
                "device_name": "devr-dev",
                "device_os": "LINUX",
                "device_os_version": "CentOS 7.6-1810",
                "device_policy": "sm-restrictive",
                "device_policy_id": 11200,
                "device_target_priority": "MEDIUM",
                "device_timestamp": "2020-08-28T19:12:41.178Z",
                "document_guid": "6Gqoe-abQXu-k9LagGOoQg",
                "filemod_count": 0,
                "ingress_time": 1598642021337,
                "modload_count": 0,
                "netconn_count": 0,
                "org_id": "test",
                "parent_effective_reputation": "NOT_LISTED",
                "parent_guid": "ABCD1234-0002b226-00000001-00000000-1d6225bbba75e43",
                "parent_hash": [
                    "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85",
                    "e4b9902024ac32b3ca37f6b4c9b841e8",
                ],
                "parent_name": "/usr/lib/systemd/systemd",
                "parent_pid": 1,
                "parent_publisher_state": ["FILE_SIGNATURE_STATE_NOT_SIGNED"],
                "parent_reputation": "NOT_LISTED",
                "process_cmdline": ["/usr/bin/gitea"],
                "process_cmdline_length": [14],
                "process_effective_reputation": "NOT_LISTED",
                "process_guid": "80dab519-3b5f-4502-afad-da87cd58a4c3",
                "process_hash": [
                    "285044ad8f8b9322d0cc5e929e2cc18c",
                    "5975d972eea6b1c53ef9a69452797439ed5bf63fae72e1780761ea1c2cb6976a",
                ],
                "process_name": "/usr/bin/bash",
                "process_pid": [10111, 10222, 10333],
                "process_publisher_state": ["FILE_SIGNATURE_STATE_NOT_SIGNED"],
                "process_reputation": "NOT_LISTED",
                "process_sha256": "5975d972eea6b1c53ef9a69452797439ed5bf63fae72e1780761ea1c2cb6976a",
                "process_start_time": "2020-05-04T21:34:03.968Z",
                "process_username": ["root"],
                "regmod_count": 0,
                "scriptload_count": 0,
            }
        ],
    }


@pytest.fixture(scope="function")
def get_process_details_0_found_resp():
    return {
        "num_found": 0,
        "results": [],
    }


@pytest.fixture(scope="function")
def delete_file_start_resp_object():
    return {
        "id": 3,
        "session_id": "1:2468",
        "device_id": 2468,
        "command_timeout": 120,
        "status": "PENDING",
        "name": "delete file",
        "object": "C:\\\\TEMP\\\\foo.txt",
        "completion_time": 0,
    }


@pytest.fixture(scope="function")
def get_kill_proc_object():
    return {
        "status": "complete",
        "values": [],
        "id": 16,
        "name": "kill",
        "result_code": 0,
        "result_desc": "",
        "sub_keys": [],
        "files": [],
        "input": {"name": "kill", "object": 3272},
        "create_time": "2021-10-29T13:56:27Z",
        "finish_time": "2021-10-29T13:56:28.105Z",
    }


@pytest.fixture(scope="function")
def get_kill_proc_wrong_pid_object():
    return {
        "status": "error",
        "values": [],
        "id": 16,
        "name": "kill",
        "result_code": 1,
        "result_desc": "",
        "sub_keys": [],
        "files": [],
        "input": {"name": "kill", "object": 3272},
        "create_time": "2021-10-29T13:56:27Z",
        "finish_time": "2021-10-29T13:56:28.105Z",
    }


@pytest.fixture(scope="function")
def get_proc_validation_object():
    return {"valid": True, "value_search_query": True}


@pytest.fixture(scope="function")
def get_proc_search_jobs_object():
    return {
        "results": [
            {
                "backend_timestamp": "2020-01-19T15:25:31.064Z",
                "childproc_count": 0,
                "crossproc_count": 40,
                "device_id": 354648,
                "device_name": "win7x64",
                "device_policy_id": 11200,
                "device_timestamp": "2020-01-18T19:46:22.885Z",
                "filemod_count": 0,
                "index_class": "default",
                "modload_count": 5,
                "netconn_count": 55380,
                "org_id": "ABCD1234",
                "parent_guid": "ABCD1234-0000a98f-000001fc-00000000-1d5cb7eca37b799",
                "parent_pid": 304,
                "partition_id": 0,
                "process_guid": "ABCD1234-0000a98f-0000051c-00000000-1d5cb7ed061e7ef",
                "process_hash": [
                    "c78655bc80301d76ed4fef1c1ea40a7d",
                    "93b2ed4004ed5f7f3039dd7ecbd22c7e4e24b6373b4d9ef8d6e45a179b13a5e8",
                ],
                "process_name": "c:\\windows\\system32\\svchost.exe",
                "process_pid": [303],
                "process_username": ["NT AUTHORITY\\LOCAL SERVICE"],
                "regmod_count": 2,
                "scriptload_count": 0,
            }
        ],
        "num_found": 760,
        "num_available": 33,
        "num_aggregated": 50,
        "approximate_unaggregated": 760,
        "contacted": 6,
        "completed": 6,
    }


@pytest.fixture(scope="function")
def start_async_proc_search_object():
    return {"job_id": "test"}


@pytest.fixture(scope="function")
def get_proc_search_status_object():
    return {
        "contacted": 22,
        "completed": 22,
        "query": {
            "cb.max_backend_timestamp": 1,
            "cb.min_backend_timestamp": 0,
            "cb.min_device_timestamp": 0,
        },
        "search_initiated_time": 0,
        "connector_id": "abcd",
    }


@pytest.fixture(scope="function")
def delete_file_end_resp_object():
    return {
        "id": 3,
        "session_id": "1:2468",
        "device_id": 2468,
        "command_timeout": 120,
        "status": "complete",
        "name": "delete file",
        "object": "C:\\\\TEMP\\\\foo.txt",
        "completion_time": 2345678901,
    }


@pytest.fixture(scope="function")
def get_list_proc_error_object():
    return {
        "id": 10,
        "session_id": "1:2468",
        "device_id": 2468,
        "command_timeout": 120,
        "status": "error",
        "name": "process list",
        "object": None,
        "completion_time": 2345678901,
        "processes": [],
    }


@pytest.fixture(scope="function")
def delete_file_error_resp_object():
    return {
        "id": 3,
        "session_id": "1:2468",
        "device_id": 2468,
        "command_timeout": 120,
        "status": "ERROR",
        "name": "delete file",
        "object": "C:\\\\TEMP\\\\foo.txt",
        "completion_time": 2345678901,
        "result_code": -2147024894,
        "result_type": "WinHresult",
        "result_desc": "File not found",
    }


@pytest.fixture(scope="function")
def get_policies_object():
    return {
        "policies": [
            {
                "id": 12345,
                "is_system": True,
                "name": "Standard",
                "description": "Test",
                "priority_level": "MEDIUM",
                "position": -1,
                "num_devices": 0,
            }
        ]
    }


@pytest.fixture(scope="function")
def get_dummy_policy_object():
    return {
        "id": 65536,
        "name": "A Dummy Policy",
        "org_key": "test",
        "version": 2,
        "priority_level": "HIGH",
        "position": -1,
        "is_system": False,
        "description": "",
        "auto_deregister_inactive_vdi_interval_ms": 0,
        "auto_delete_known_bad_hashes_delay": 86400000,
        "av_settings": {
            "avira_protection_cloud": {
                "enabled": True,
                "max_exe_delay": 45,
                "max_file_size": 4,
                "risk_level": 4,
            },
            "on_access_scan": {"enabled": True, "mode": "AGGRESSIVE"},
            "on_demand_scan": {
                "enabled": True,
                "profile": "NORMAL",
                "schedule": {
                    "start_hour": 0,
                    "range_hours": 0,
                    "recovery_scan_if_missed": True,
                },
                "scan_usb": "AUTOSCAN",
                "scan_cd_dvd": "AUTOSCAN",
            },
            "signature_update": {
                "enabled": True,
                "schedule": {
                    "full_interval_hours": 0,
                    "initial_random_delay_hours": 1,
                    "interval_hours": 2,
                },
            },
            "update_servers": {
                "servers_override": [],
                "servers_for_onsite_devices": [
                    {
                        "server": "http://updates2.cdc.carbonblack.io/update2",
                        "preferred": False,
                    }
                ],
                "servers_for_offsite_devices": [
                    "http://updates2.cdc.carbonblack.io/update2"
                ],
            },
        },
        "rules": [
            {
                "id": 1,
                "required": True,
                "action": "DENY",
                "application": {"type": "REPUTATION", "value": "PUP"},
                "operation": "MEMORY_SCRAPE",
            },
            {
                "id": 2,
                "required": True,
                "action": "DENY",
                "application": {"type": "NAME_PATH", "value": "data"},
                "operation": "MEMORY_SCRAPE",
            },
        ],
        "directory_action_rules": [
            {"file_upload": False, "protection": False, "path": ""}
        ],
        "sensor_settings": [
            {"name": "ALLOW_UNINSTALL", "value": "true"},
            {"name": "ALLOW_UPLOADS", "value": "false"},
            {"name": "SHOW_UI", "value": "true"},
            {"name": "ENABLE_THREAT_SHARING", "value": "true"},
            {"name": "QUARANTINE_DEVICE", "value": "false"},
            {"name": "LOGGING_LEVEL", "value": "false"},
            {
                "name": "QUARANTINE_DEVICE_MESSAGE",
                "value": "Your device has been quarantined. Please contact your administrator.",
            },
            {"name": "SET_SENSOR_MODE", "value": "0"},
            {"name": "SENSOR_RESET", "value": "0"},
            {"name": "BACKGROUND_SCAN", "value": "true"},
            {"name": "POLICY_ACTION_OVERRIDE", "value": "true"},
            {"name": "HELP_MESSAGE", "value": ""},
            {"name": "PRESERVE_SYSTEM_MEMORY_SCAN", "value": "false"},
            {"name": "HASH_MD5", "value": "true"},
            {"name": "SCAN_LARGE_FILE_READ", "value": "false"},
            {"name": "SCAN_EXECUTE_ON_NETWORK_DRIVE", "value": "true"},
            {"name": "DELAY_EXECUTE", "value": "false"},
            {"name": "SCAN_NETWORK_DRIVE", "value": "true"},
            {"name": "BYPASS_AFTER_LOGIN_MINS", "value": "0"},
            {"name": "BYPASS_AFTER_RESTART_MINS", "value": "0"},
            {"name": "SHOW_FULL_UI", "value": "true"},
            {"name": "SECURITY_CENTER_OPT", "value": "true"},
            {"name": "CB_LIVE_RESPONSE", "value": "true"},
            {"name": "UNINSTALL_CODE", "value": "false"},
            {"name": "UBS_OPT_IN", "value": "true"},
            {"name": "ALLOW_EXPEDITED_SCAN", "value": "true"},
        ],
        "rapid_configs": [],
    }
