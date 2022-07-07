import datetime
import time
import array

from plantstar_shared.global_definitions import utc_now

TEN_MILLISECONDS = .01


class MockRawDataProcessor:
    class EmptyInputSignalDictionaries(Exception):
        pass

    def __init__(
        self, cycle_time_in_milliseconds=30000, number_of_digital_inputs=16, number_of_digital_outputs=8, number_of_analog_inputs=32, debounce_raw_buffer_size=255,
        analog_value_min=50, analog_value_max=2, analog_value_step=0.5
    ):
        self.next_value_swap_in_seconds_timedelta = datetime.timedelta(milliseconds=cycle_time_in_milliseconds / 2)
        self.next_value_swap_datetime = utc_now() + self.next_value_swap_in_seconds_timedelta

        self.number_of_digital_inputs = number_of_digital_inputs
        self.number_of_digital_outputs = number_of_digital_outputs
        self.number_of_analog_inputs = number_of_analog_inputs
        self.debounce_raw_buffer_size = debounce_raw_buffer_size
        self.analog_value_min = analog_value_min
        self.analog_value_max = analog_value_max
        self.analog_value_step = analog_value_step

        self.last_digital_input_debounce_array = array.array("B", [0 for _ in range(self.number_of_digital_inputs)])
        self.last_digital_output_array = array.array("B", [0 for _ in range(self.number_of_digital_outputs)])
        self.last_analog_filter_array = array.array("B", [0 for _ in range(self.number_of_analog_inputs)])
        self.last_analog_gain_array = array.array("B", [0 for _ in range(self.number_of_analog_inputs)])

        self.state_on_or_off_value = False
        self.current_analog_value = analog_value_max
        self.current_analog_step_direction = -1
        self.cold_end_value = 20

    def check_data_length_and_limit(self, input_data_buffer, data_buffer_length_limit, data_buffer_int_limit):
        if len(input_data_buffer) == data_buffer_length_limit:
            for i in range(data_buffer_length_limit):
                if input_data_buffer[i] < 0 or input_data_buffer[i] > data_buffer_int_limit:
                    raise ValueError(f"Incorrect value passed into array.array object. It must be 0 through {data_buffer_int_limit}.")
        else:
            raise ValueError(
                "Expected a memory view with {0} items, {1}{2} were received.".format(
                    data_buffer_length_limit, "only " if len(input_data_buffer) < data_buffer_length_limit else "", len(input_data_buffer)
                )
            )

    def upload_new_driver_settings(self, data_type_string, data_buffer):
        if data_type_string == "digital_outputs":
            data_buffer_len = self.number_of_digital_outputs
            data_buffer_int_limit = 1
            self.check_data_length_and_limit(data_buffer, data_buffer_len, data_buffer_int_limit)

            if self.last_digital_output_array != data_buffer:
                self.last_digital_output_array = data_buffer
        elif data_type_string == "analog_gains":
            data_buffer_len = self.number_of_analog_inputs
            data_buffer_int_limit = 3
            self.check_data_length_and_limit(data_buffer, data_buffer_len, data_buffer_int_limit)

            if self.last_analog_gain_array != data_buffer:
                self.last_analog_gain_array = data_buffer
        elif data_type_string == "analog_filters":
            data_buffer_len = self.number_of_analog_inputs
            data_buffer_int_limit = 15
            self.check_data_length_and_limit(data_buffer, data_buffer_len, data_buffer_int_limit)

            if self.last_analog_filter_array != data_buffer:
                self.last_analog_filter_array = data_buffer
        elif data_type_string == "digital_input_debounce":
            data_buffer_len = self.number_of_digital_inputs
            data_buffer_int_limit = self.debounce_raw_buffer_size - 1
            self.check_data_length_and_limit(data_buffer, data_buffer_len, data_buffer_int_limit)

            if self.last_digital_input_debounce_array != data_buffer:
                self.last_digital_input_debounce_array = data_buffer
        else:
            if type(data_type_string) == str:
                raise ValueError(
                    f"An Incorrect value of {data_type_string} was passed. This function expects \"digital_outputs\", \"analog_gains\", or \"analog_filters\"."
                )
            else:
                raise TypeError(
                    f"Failed to pass a recognizable type of data. {data_type_string} was passed in with a {type(data_type_string)} data type. This function expects a string "
                    f"of \"digital_outputs\", \"analog_gains\", or \"analog_filters\"."
                )

    def get_input_signal_dictionaries(self):
        time.sleep(TEN_MILLISECONDS)

        the_now = utc_now()

        if self.next_value_swap_datetime <= the_now:
            self.state_on_or_off_value = not self.state_on_or_off_value
            self.next_value_swap_datetime = the_now + self.next_value_swap_in_seconds_timedelta

            if self.state_on_or_off_value:
                self.current_analog_value = self.analog_value_max
                self.current_analog_step_direction = -1

        return_dictionary = {
            1: {
                "digitals": {str(state_index + 1): int(self.state_on_or_off_value) for state_index in range(16)},
                "analogs": {str(state_index + 1): self.current_analog_value for state_index in range(24)},
                "cold_end": {str(state_index + 1): self.cold_end_value for state_index in range(24)},
                "event_unix_timestamp": the_now.timestamp()
            }
        }

        self.step_current_analog_value()

        return return_dictionary

    def get_driver_version_string(self):
        return "Mock"

    def get_version_string(self):
        return "Mock"

    def step_current_analog_value(self):
        if self.current_analog_step_direction == -1:
            step_min_max_function = max
            ceiling_or_floor_value = self.analog_value_min
        else:
            step_min_max_function = min
            ceiling_or_floor_value = self.analog_value_max

        new_analog_value = step_min_max_function(self.current_analog_value + self.analog_value_step * self.current_analog_step_direction, ceiling_or_floor_value)

        if new_analog_value == ceiling_or_floor_value:
            self.current_analog_step_direction *= -1

        self.current_analog_value = new_analog_value
