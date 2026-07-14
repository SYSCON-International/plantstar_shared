class RequestDataKeys:
    # Envelope (identity) — present on every request
    DEVICE_TYPE = "device_type"
    DEVICE_IP_ADDRESS = "device_ip_address"
    USERNAME = "username"
    # Signing — injected by send_post_request, read by validate_request
    SIGNED_STRING = "signed_string"
    SIGNER_TIMESTAMP = "signer_timestamp"
    # Payload fields — endpoint-specific, still standardized
    DEVICE_NAME = "device_name"
    IS_COLDBOOTING = "is_coldbooting"
    IS_INITIALIZING = "is_initializing"
    MESSAGE_DICTIONARY = "message_dictionary"
    SHOULD_ONLY_SEND_IF_PROCESSES_STARTED = "should_only_send_if_processes_started"


class DeviceTypes:
    DATA_COLLECTION_MODULE = "dcm"
    HMI = "hmi"


def build_api_request_data(*, device_type, device_ip_address, username, payload=None):
    data = {
        RequestDataKeys.DEVICE_TYPE: device_type,
        RequestDataKeys.DEVICE_IP_ADDRESS: device_ip_address,
        RequestDataKeys.USERNAME: username,
    }

    if payload:
        data.update(payload)

    return data
