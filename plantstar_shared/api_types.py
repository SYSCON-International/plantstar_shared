import enum
from attr import has
import requests

from django.core.signing import Signer
from django.utils.timezone import now

from plantstar_shared.is_valid_signed_string import is_valid_signed_string


# TODO: Inherit from SyconType
class ApiTypes(enum.Enum):
    @staticmethod
    def send_get_request(api_type_name, ip_address, timeout=None, data=None, signer_key=None, logger=None):
        return ApiTypes.send_get_post_request_base(
            api_type_name=api_type_name, ip_address=ip_address, request_function=requests.get, timeout=timeout, data=data, signer_key=signer_key, logger=logger
        )

    @staticmethod
    def send_post_request(api_type_name, ip_address, timeout=None, data=None, signer_key=None, logger=None):
        return ApiTypes.send_get_post_request_base(
            api_type_name=api_type_name, ip_address=ip_address, request_function=requests.post, timeout=timeout, data=data, signer_key=signer_key, logger=logger
        )

    @staticmethod
    def send_get_post_request_base(*, api_type_name, ip_address, request_function, timeout=None, data=None, signer_key=None, logger=None):
        request_url = f"http://{ip_address}/{api_type_name}/"

        if signer_key:
            signer_timestamp = str(now().timestamp())
            signed_string = Signer(key=signer_key, salt=signer_timestamp).sign(api_type_name)

            if data is None:
                data = {}

            data["signed_string"] = signed_string
            data["signer_timestamp"] = signer_timestamp

        try:
            request = request_function(request_url, timeout=timeout, data=data)
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

    @staticmethod
    def is_valid_request(*, api_type_name, signer_key, data):
        signed_string = data.get("signed_string", None)
        signer_timestamp = data.get("signer_timestamp", None)

        if signed_string and signer_timestamp:
            return is_valid_signed_string(signer_key=signer_key, signed_string=signed_string, unsigned_string=api_type_name, salt=signer_timestamp)
        elif signed_string is None and signer_timestamp is None:
            return True

        return False


class DataCollectionModuleApiTypes(ApiTypes):
    GET_DATA_COLLECTION_MODULE_SYSTEM_DISK_USAGE = "get_data_collection_module_system_disk_usage"
    GET_DATA_COLLECTION_MODULE_SYSTEM_INFORMATION = "get_data_collection_module_system_information"
    GET_SYSTEM_ERROR_DICTIONARY_LIST = "get_system_error_dictionary_list"

    GET_DATA_COLLECTION_MODULE_PROCESS_STATUSES = "get_data_collection_module_process_statuses"
    COLDBOOT_DATA_COLLECTION_MODULE = "coldboot_data_collection_module"
    REBOOT_DATA_COLLECTION_MODULE = "reboot_data_collection_module"


class ApuApiTypes(ApiTypes):
    SET_IS_INITIALIZING_STATUS = "set_is_initializing_status"
    SET_IS_COLDBOOTING_STATUS = "set_is_coldbooting_status"
