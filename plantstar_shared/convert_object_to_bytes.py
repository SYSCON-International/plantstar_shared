from plantstar_shared import syscon_json

# Converts the output dictionary into a string through syscon_json.dumps, then encodes it into bytes so that it can be sent through the socket, and parsed later on
def convert_object_to_bytes(input_object, encoding_format="ASCII"):
    input_object_as_string = syscon_json.dumps(input_object)
    input_object_as_bytes = input_object_as_string.encode(encoding_format)

    return input_object_as_bytes
