import msgpack

from plantstar_shared.errors import SocketConnectionError


# Converts bytes into an object using msgpack, with a parameter for strict_map_key
def convert_bytes_to_object(object_as_bytes, strict_map_key=False):
    if not object_as_bytes:
        raise SocketConnectionError
    
    output_object = msgpack.unpackb(object_as_bytes, strict_map_key=strict_map_key)
    return output_object
