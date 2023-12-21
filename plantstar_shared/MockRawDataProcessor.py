import datetime
import time
import array
from itertools import chain, repeat, islice

from plantstar_shared.global_definitions import utc_now

TEN_MILLISECONDS = .01


class MockRawDataProcessor:
    def __init__(
        self, cycle_time_in_milliseconds=30000, number_of_digital_inputs=200, number_of_digital_outputs=200, number_of_analog_inputs=200, debounce_raw_buffer_size=255,
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

        self.last_digital_input_debounce_array = array.array("B", pad([0 for _ in range(self.number_of_digital_inputs)], self.debounce_raw_buffer_size, 0))
        self.last_digital_output_array = array.array("B", pad([0 for _ in range(self.number_of_digital_outputs)], self.debounce_raw_buffer_size, 0))
        self.last_analog_filter_array = array.array("B", pad([0 for _ in range(self.number_of_analog_inputs)], self.debounce_raw_buffer_size, 0))
        self.last_analog_gain_array = array.array("B", pad([0 for _ in range(self.number_of_analog_inputs)], self.debounce_raw_buffer_size, 0))

        self.state_on_or_off_value = False
        self.current_analog_value = analog_value_max
        self.current_analog_step_direction = -1
        self.cold_end_value = 20

    def upload_new_driver_settings(self, data_type_string, data_buffer):
        data_buffer_array = array.array("B", list(pad(data_buffer, self.debounce_raw_buffer_size, 0)))

        if data_type_string == "digital_outputs":
            if self.last_digital_output_array != data_buffer_array:
                self.last_digital_output_array = data_buffer_array
        elif data_type_string == "analog_gains":
            if self.last_analog_gain_array != data_buffer_array:
                self.last_analog_gain_array = data_buffer_array
        elif data_type_string == "analog_filters":
            if self.last_analog_filter_array != data_buffer_array:
                self.last_analog_filter_array = data_buffer_array
        elif data_type_string == "digital_input_debounce":
            if self.last_digital_input_debounce_array != data_buffer_array:
                self.last_digital_input_debounce_array = data_buffer_array
        else:
            if isinstance(data_type_string, str):
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

        return_input_signal_dictionary_list = [
            {
                "analogs": [self.current_analog_value for _ in range(self.debounce_raw_buffer_size)],
                "cold_ends": [self.cold_end_value for _ in range(self.debounce_raw_buffer_size)],
                "digitals": [self.state_on_or_off_value for _ in range(self.debounce_raw_buffer_size)],
                "event_unix_timestamp": the_now.timestamp()
            }
        ]

        self.step_current_analog_value()

        return return_input_signal_dictionary_list

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


def pad(iterable, size, padding=None):
    return islice(pad_infinite(iterable, padding), size)


def pad_infinite(iterable, padding=None):
    return chain(iterable, repeat(padding))
