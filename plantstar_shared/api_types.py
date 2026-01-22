import requests

from django.core.signing import Signer
from plantstar_shared.SysconType import SysconTypeOld
from plantstar_shared.errors import InvalidApiRequest, SysconProgrammingError
from plantstar_shared.is_valid_signed_string import is_valid_signed_string
from plantstar_shared.global_definitions import safe_now


def send_get_request(api_type, ip_address, connect_timeout=2, read_timeout=10, data=None, signer_key=None, logger=None, use_https=False):
    return _send_get_post_request_base(
        api_type=api_type, ip_address=ip_address, request_function=requests.get, connect_timeout=connect_timeout, read_timeout=read_timeout, data=data, signer_key=signer_key,
        logger=logger,  use_https=use_https
    )


def send_post_request(api_type, ip_address, connect_timeout=2, read_timeout=10, data=None, signer_key=None, logger=None, use_https=False):
    return _send_get_post_request_base(
        api_type=api_type, ip_address=ip_address, request_function=requests.post, connect_timeout=connect_timeout, read_timeout=read_timeout, data=data, signer_key=signer_key,
        logger=logger, use_https=use_https
    )


def _send_get_post_request_base(*, api_type, ip_address, request_function, connect_timeout=2, read_timeout=10, data=None, signer_key=None, logger=None, use_https=False):
    should_sign = api_type.value[2]

    if should_sign and not signer_key:
        raise SysconProgrammingError("This API call requires a signer_key, but one was not provided")
    elif not should_sign and signer_key:
        raise SysconProgrammingError("This API should not have a signer_key, but one was provided")

    if use_https:
        http_prefix = "https"
    else:
        http_prefix = "http"

    api_type_name = api_type.value[0]

    request_url = f"{http_prefix}://{ip_address}/{api_type_name}/"

    if signer_key:
        signer_timestamp = str(safe_now().timestamp())
        signed_string = Signer(key=signer_key, salt=signer_timestamp).sign(api_type_name)

        if data is None:
            data = {}

        data["signed_string"] = signed_string
        data["signer_timestamp"] = signer_timestamp

    try:
        request = request_function(request_url, timeout=(connect_timeout, read_timeout), data=data)
    except Exception as error:
        error_message = f"The API request \"{api_type_name}\" sent to \"{request_url}\" failed with error: {error}"

        if logger is not None:
            logger.error(error_message)

        raise error

    try:
        data_dictionary = request.json()
    except:
        data_dictionary = {}

    return request.status_code, data_dictionary


def validate_request(*, api_type, signer_key, data):
    should_sign = api_type.value[2]

    signed_string = data.get("signed_string", None)
    signer_timestamp = data.get("signer_timestamp", None)

    if should_sign and (not signed_string or not signer_timestamp):
        raise InvalidApiRequest(f"This API call requires a signed_string and signer_timestamp, but {signed_string} and {signer_timestamp} were provided")
    elif not should_sign and (signed_string or signer_timestamp):
        raise InvalidApiRequest(f"This API call should not have a signed_string or signer_timestamp, but {signed_string} and {signer_timestamp} were provided")

    if signed_string and signer_timestamp:
        api_type_name = api_type.value[0]

        if not is_valid_signed_string(signer_key=signer_key, signed_string=signed_string, unsigned_string=api_type_name, salt=signer_timestamp):
            raise InvalidApiRequest(f"Invalid signing: signer_key: {signer_key}, signed_string: {signed_string}, unsigned_string: {api_type_name}, salt: {signer_timestamp}")


class DataCollectionModuleApiTypes(SysconTypeOld):
    GET_DATA_COLLECTION_MODULE_SYSTEM_DISK_USAGE = ("get_data_collection_module_system_disk_usage", "get_data_collection_module_system_disk_usage", True)
    GET_DATA_COLLECTION_MODULE_SYSTEM_INFORMATION = ("get_data_collection_module_system_information", "get_data_collection_module_system_information", True)
    SET_DATA_COLLECTION_MODULE_SYSTEM_INFORMATION = ("set_data_collection_module_system_information", "set_data_collection_module_system_information", True)
    GET_SYSTEM_ERROR_DICTIONARY_LIST = ("get_system_error_dictionary_list", "get_system_error_dictionary_list", True)

    GET_DATA_COLLECTION_MODULE_PROCESS_STATUSES = ("get_data_collection_module_process_statuses", "get_data_collection_module_process_statuses", True)
    COLDBOOT_DATA_COLLECTION_MODULE = ("coldboot_data_collection_module", "coldboot_data_collection_module", True)
    REBOOT_DATA_COLLECTION_MODULE = ("reboot_data_collection_module", "reboot_data_collection_module", True)


class ApuApiTypes(SysconTypeOld):
    SET_IS_INITIALIZING_STATUS = ("data_collection_module_manager/set_is_initializing_status", "data_collection_module_manager/set_is_initializing_status", True)
    SET_IS_COLDBOOTING_STATUS = ("data_collection_module_manager/set_is_coldbooting_status", "data_collection_module_manager/set_is_coldbooting_status", True)
    REGISTER_HMI = ("data_collection_module_manager/register_hmi", "data_collection_module_manager/register_hmi", True)
    REGISTER_DCM = ("data_collection_module_manager/register_dcm", "data_collection_module_manager/register_dcm", True)
    SEND_TEAMS_MESSAGE = ("base_app/send_teams_message", "base_app/send_teams_message", True)
    GET_USER_FINGERPRINTS = ("user_manager/get_user_fingerprints", "user_manager/get_user_fingerprints", True)
    ADD_USER_FINGERPRINT = ("user_manager/add_user_fingerprint", "user_manager/add_user_fingerprint", False)
    DELETE_USER_FINGERPRINT = ("user_manager/delete_user_fingerprint", "user_manager/delete_user_fingerprint", True)
    RELABEL_USER_FINGERPRINT = ("user_manager/relabel_user_fingerprint", "user_manager/relabel_user_fingerprint", True)
    IDENTIFY_USER_FINGERPRINT = ("user_manager/identify_user_fingerprint", "user_manager/identify_user_fingerprint", False)


class CosmosApiTypes(SysconTypeOld):
    SEND_DATA_DICTIONARY = ("send_data_dictionary", "send_data_dictionary", True)


class HmiApiTypes(SysconTypeOld):
    IDENTIFY_FINGERPRINT = ("identify_fingerprint", "identify_fingerprint", True)
    ADD_FINGERPRINT = ("add_fingerprint", "add_fingerprint", True)
    GET_HMI_SYSTEM_INFORMATION = ("get_hmi_system_information", "get_hmi_system_information", True)
    SET_HMI_SYSTEM_INFORMATION = ("set_hmi_system_information", "set_hmi_system_information", True)
    REBOOT_HMI = ("reboot_hmi", "reboot_hmi", True)

