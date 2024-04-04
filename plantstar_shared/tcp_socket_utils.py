import struct

from plantstar_shared.convert_bytes_to_object import convert_bytes_to_object
from plantstar_shared.convert_object_to_bytes import convert_object_to_bytes
from plantstar_shared.errors import SocketConnectionError

SIZE_OF_UNSIGNED_INT_STRUCT = 4  # size of integer value that precedes data coming from DCM


def read_size_value_from_socket(*, remote_socket, is_big_endian, number_of_bytes_for_size_prefix):
    size_bytes = remote_socket.recv(number_of_bytes_for_size_prefix)

    if not size_bytes:
        return None

    if number_of_bytes_for_size_prefix == 2:
        message_length = int.from_bytes(size_bytes, 'big') if is_big_endian else int.from_bytes(size_bytes, 'little')
    elif number_of_bytes_for_size_prefix == SIZE_OF_UNSIGNED_INT_STRUCT:
        number_format = ">I" if is_big_endian else "<I"

        try:
            message_length = struct.unpack(number_format, size_bytes)[0]
        except struct.error as error:
            raise SocketConnectionError
    else:
        raise SysconProgrammingError("A size prefix was set to something other than 2 or 4")

    return message_length


def get_message_from_socket(*, remote_socket):
    message_length = read_size_value_from_socket(remote_socket=remote_socket)

    if not message_length:
        return None

    packets = []
    bytes_received = 0

    # While loop that will stream in data if the full request is not available yet
    while bytes_received < message_length:
        buffer_size = message_length - bytes_received
        packet = remote_socket.recv(buffer_size)

        if not packet:
            return None

        packets.append(packet)
        bytes_received = bytes_received + len(packet)

    data = b''.join(packets)
    return data


def send_message_on_socket(*, remote_socket, dumpsable_object):
    message_encoded_as_bytes = convert_object_to_bytes(dumpsable_object)
    send_encoded_message_on_socket(remote_socket=remote_socket, encoded_message=message_encoded_as_bytes)


def send_encoded_message_on_socket(*, remote_socket, encoded_message):
    size_of_string = len(encoded_message)
    encoded_message_with_size = struct.pack('>I', size_of_string) + encoded_message

    bytes_sent = remote_socket.send(encoded_message_with_size)

    while bytes_sent < size_of_string + SIZE_OF_UNSIGNED_INT_STRUCT:
        remaining_encoded_message_to_send = encoded_message_with_size[bytes_sent:]
        new_bytes_sent = remote_socket.send(remaining_encoded_message_to_send)
        bytes_sent += new_bytes_sent


def get_object_from_socket(*, remote_socket):
    object_from_interface_as_bytes = get_message_from_socket(remote_socket=remote_socket)
    object_from_interface = convert_bytes_to_object(object_from_interface_as_bytes)
    return object_from_interface
