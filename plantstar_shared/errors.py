class InvalidApiRequest(Exception):
    pass


class SysconProgrammingError(Exception):
    pass


def raise_invalid_type_error(the_type, invalid_type_supplied):
    raise SysconProgrammingError(f"Invalid \"{the_type.__name__}\" type: \"{invalid_type_supplied}\"")
