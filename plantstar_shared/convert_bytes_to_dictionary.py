from plantstar_shared import syscon_json

# Converts bytes into a decoded string, then into a dictionary using syscon_json.loads
def convert_bytes_to_dictionary(output_dictionary_as_bytes, decoding_format="ASCII"):
    output_dictionary_as_string = output_dictionary_as_bytes.decode(decoding_format)
    output_dictionary = syscon_json.loads(output_dictionary_as_string)

    return output_dictionary
