from plantstar_shared import syscon_json

# Converts the output dictionary into a string through syscon_json.dumps, then encodes it into bytes so that it can be sent through the socket, and parsed later on
def convert_dictionary_to_bytes(output_dictionary, encoding_format="ASCII"):
    output_dictionary_as_string = syscon_json.dumps(output_dictionary)
    output_dictionary_as_bytes = output_dictionary_as_string.encode(encoding_format)

    return output_dictionary_as_bytes
