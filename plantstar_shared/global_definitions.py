import datetime
import inspect

import pytz
from django.utils.timezone import now

from plantstar_shared import syscon_json


def utc_now():
    return datetime.datetime.now(pytz.utc)


def safe_now():
    """If Django's `now()` throws an exception, we default to `utc_now()`.  Calling Django's `now()` will throw an exception when calling it in non-Django environments."""
    try:
        return now()
    except Exception:
        return utc_now()


def convert_to_json(the_class):
    base_dictionary = dict((key, value) for key, value in inspect.getmembers(the_class()) if not key.startswith("__") and not inspect.isfunction(value))

    return syscon_json.dumps(base_dictionary, default=lambda _: "Not Serializeable")


# TODO: Inherit from SyconType and remove `convert_to_json``
class StatusCodes:
    OK = 200
    MOVED_PERMANENTLY = 301
    FOUND = 302
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

    @staticmethod
    def convert_to_json():
        return convert_to_json(StatusCodes)
