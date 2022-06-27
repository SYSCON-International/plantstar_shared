from plantstar_shared.RawDataProcessorInterfaceActions import RawDataProcessorInterfaceActions
from plantstar_shared.errors import SysconProgrammingError


def obtain_raw_data_processor_function_for_action_name(rawdataprocessor, action_name):
    if action_name == RawDataProcessorInterfaceActions.GET_DRIVER_VERSION_STRING:
        return rawdataprocessor.get_driver_version_string
    elif action_name == RawDataProcessorInterfaceActions.GET_INPUT_SIGNAL_DICTIONARIES:
        return rawdataprocessor.get_input_signal_dictionaries
    elif action_name == RawDataProcessorInterfaceActions.GET_VERSION_STRING:
        return rawdataprocessor.get_version_string
    elif action_name == RawDataProcessorInterfaceActions.UPDATE_ANALOG_INPUTS:
        return rawdataprocessor.update_analog_inputs
    elif action_name == RawDataProcessorInterfaceActions.UPDATE_DIGITAL_INPUT_DEBOUNCE:
        return rawdataprocessor.update_digital_input_debounce
    elif action_name == RawDataProcessorInterfaceActions.UPLOAD_NEW_DRIVER_SETTINGS:
        return rawdataprocessor.upload_new_driver_settings
    else:
        raise SysconProgrammingError
