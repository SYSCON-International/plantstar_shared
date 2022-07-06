from plantstar_shared import syscon_json

# Converts bytes into a decoded string, then into an object using syscon_json.loads
def convert_bytes_to_object(object_as_encoded_string, decoding_format="ASCII"):
    object_as_decoded_string = object_as_encoded_string.decode(decoding_format)
    output_object = syscon_json.loads(object_as_decoded_string)

    return output_object
