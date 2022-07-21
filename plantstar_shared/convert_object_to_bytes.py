import msgpack

# Converts the output dictionary into bytes using msgpack
def convert_object_to_bytes(input_object):
    input_object_as_bytes = msgpack.packb(input_object)
    return input_object_as_bytes
