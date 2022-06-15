import enum

class RawDataProcessorInterfaceActions(enum.Enum):
    GET_DRIVER_VERSION_STRING = "get_driver_version_string"
    GET_INPUT_SIGNAL_DICTIONARIES = "get_input_signal_dictionaries"
    GET_MOCK_RAW_DATA_PROCESSOR_STATUS = "get_mock_raw_data_processor_status"
    GET_VERSION_STRING = "get_version_string"
    UPDATE_ANALOG_INPUTS = "update_analog_inputs"
    UPDATE_DIGITAL_INPUT_DEBOUNCE = "update_digital_input_debounce"
    UPLOAD_NEW_DRIVER_SETTINGS = "upload_new_driver_settings"
