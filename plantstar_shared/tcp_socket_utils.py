import struct

from plantstar_shared.convert_bytes_to_object import convert_bytes_to_object
from plantstar_shared.convert_object_to_bytes import convert_object_to_bytes
from plantstar_shared.errors import SocketConnectionError, SysconProgrammingError

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


def get_bytes_from_socket(*, remote_socket, number_of_bytes_to_read=None, is_big_endian=True, number_of_bytes_for_size_prefix=0, should_remove_prefix_size_from_read=False):
    """Obtains a number of bytes from a provided socket, with options for different configurations and situations

    Keywords / Example Configurations:
        remote_socket -- the connection that bytes will be read from

        number_of_bytes_to_read -- the number of bytes to read on the socket, if this is known, this is the only optional parameter needed (default: 0)

        is_big_endian -- bool that determines what format string should be used for unpacking the size value (default: True)

        number_of_bytes_for_size_prefix -- the number of bytes to read to determine the total size of the message to pass (default: 0)

        should_remove_prefix_size_from_read -- bool that determines if the size should be removed from the calculated number of bytes to read (default: False)

        -----

        get_bytes_from_socket(remote_socket=conn, number_of_bytes_to_read=100) - likely would not be called directly, in most cases

        get_bytes_from_socket(remote_socket=conn, is_big_endian=True, number_of_bytes_for_size_prefix=4) - reads 4 bytes to get the size, then reads that amount (DCM socket, etc)

        get_bytes_from_socket(remote_socket=conn, is_big_endian=False, number_of_bytes_for_size_prefix=2, should_remove_prefix_size_from_read=True) - reads 2 bytes to get the size,
        then reads that calculated amount minus 2 (Husky socket, etc)

    """

    if not number_of_bytes_to_read:
        if number_of_bytes_for_size_prefix:
            number_of_bytes_to_read = read_size_value_from_socket(
                remote_socket=remote_socket, is_big_endian=is_big_endian, number_of_bytes_for_size_prefix=number_of_bytes_for_size_prefix
            )

    if not number_of_bytes_to_read:
        raise SysconProgrammingError("get_bytes_from_socket was called with no parameters for number_of_bytes_to_read or number_of_bytes_for_size_prefix")

    if should_remove_prefix_size_from_read:
        number_of_bytes_to_read = number_of_bytes_to_read - number_of_bytes_for_size_prefix

    packets = []
    bytes_received = 0

    # While loop that will stream in data if the full request is not available yet
    while bytes_received < number_of_bytes_to_read:
        buffer_size = number_of_bytes_to_read - bytes_received
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
    """Function that is used between the APU and DCM to send dictionaries """
    object_from_interface_as_bytes = get_bytes_from_socket(remote_socket=remote_socket, is_big_endian=True, number_of_bytes_for_size_prefix=SIZE_OF_UNSIGNED_INT_STRUCT)
    object_from_interface = convert_bytes_to_object(object_from_interface_as_bytes)
    return object_from_interface
