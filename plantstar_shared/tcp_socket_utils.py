import struct

from add_size_onto_string_and_return.add_size_onto_string_and_return import add_size_onto_string_and_return
from convert_bytes_to_object.convert_bytes_to_object import convert_bytes_to_object
from convert_object_to_bytes.convert_object_to_bytes import convert_object_to_bytes


SIZE_OF_UNSIGNED_INT_STRUCT = 4


def read_size_value_from_socket(*, remote_socket):
    size_struct = remote_socket.recv(SIZE_OF_UNSIGNED_INT_STRUCT)

    if not size_struct:
        return None

    message_length = struct.unpack('>I', size_struct)[0]
    return message_length

def get_message_from_socket(*, remote_socket):
    message_length = read_size_value_from_socket(remote_socket)

    data = bytearray()

    # While loop that will stream in data if the full request is not available yet
    while len(data) < message_length:
        packet = remote_socket.recv(message_length - len(data))

        if not packet:
            return None

        data.extend(packet)
    return data

def send_message_on_socket(*, remote_socket, dumpsable_object, encoding='ASCII'):
    encoded_message = convert_object_to_bytes(input_object=message, encoding_format=encoding)
    send_encoded_message_on_socket(remote_socket=remote_socket, encoded_message=encoded_message)

def send_encoded_message_on_socket(*, remote_socket, encoded_message):
    size_of_message = add_size_onto_string_and_return(encoded_message)
    remote_socket.send(encoded_message)

def get_output_dictionary_from_encoded_message():
    output_dictionary_from_interface_as_bytes = get_message_from_socket(remote_socket=remote_socket)
    output_dictionary_from_interface = convert_bytes_to_object(output_from_interface_as_bytes)
    return output_dictionary_from_interface