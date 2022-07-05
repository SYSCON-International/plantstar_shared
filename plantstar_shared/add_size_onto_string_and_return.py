import struct

# Creates a message that is comprised of the size of an encoded string + that encoded string for use in sending messages over TCP sockets
def add_size_onto_string_and_return(encoded_string):
    size_of_string = len(encoded_string)
    encoded_string_prepended_with_size = struct.pack('>I', size_of_string) + encoded_string
    return encoded_string_prepended_with_size
