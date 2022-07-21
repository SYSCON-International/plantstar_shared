class InvalidApiRequest(Exception):
    pass


class SocketConnectionError(Exception):
    pass



class SysconProgrammingError(Exception):
    pass

    @staticmethod
    def get_invalid_type_error(the_type, invalid_type_supplied):
        return SysconProgrammingError(f"Invalid \"{the_type.__name__}\" type: \"{invalid_type_supplied}\"")
