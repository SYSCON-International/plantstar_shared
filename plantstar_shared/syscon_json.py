import json
import datetime
import uuid
import pytz
from dateutil.tz import tzutc
from psycopg2._range import DateTimeTZRange

from plantstar_shared.syscon_image_field import SysconImageFieldFile


class SysconEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj is None:
            return None

        if hasattr(obj, "tzinfo"):
            # This is here for a weird bug that was happening
            if obj.tzinfo == tzutc:
                tzinfo = "UTC"
            elif isinstance(obj.tzinfo, datetime.timezone):
                if obj.tzinfo.tzname(None) in ["+0000", "UTC"]:
                    tzinfo = "UTC"
                else:
                    raise Exception("Fixed offset is not utc, we need to figure out how to solve this issue.")
            else:
                tzinfo = str(obj.tzinfo)
        else:
            tzinfo = "UTC"

        if isinstance(obj, datetime.datetime):
            return {
                "__type__": "datetime",
                "year": obj.year,
                "month": obj.month,
                "day": obj.day,
                "hour": obj.hour,
                "minute": obj.minute,
                "second": obj.second,
                "microsecond": obj.microsecond,
                "tzinfo": tzinfo
            }
        elif isinstance(obj, datetime.date):
            return {
                "__type__": "date",
                "year": obj.year,
                "month": obj.month,
                "day": obj.day
            }
        elif isinstance(obj, datetime.time):
            return {
                "__type__": "time",
                "hour": obj.hour,
                "minute": obj.minute,
                "second": obj.second,
                "microsecond": obj.microsecond,
                "tzinfo": tzinfo
            }
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, DateTimeTZRange):
            return {
                "__type__": "datetime_range",
                "lower": obj.lower,
                "upper": obj.upper,
                "bounds": obj._bounds
            }
        elif isinstance(obj, SysconImageFieldFile):
            if obj:
                return {
                    "__type__": "SysconImageFieldFile",
                    "path": obj.src_path
                }
            else:
                return ""
        else:
            return super(SysconEncoder, self).default(obj)


class SysconDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.decode_special_types)

    def decode_special_types(self, dictionary):
        if "__type__" not in dictionary:
            return dictionary

        type_name = dictionary.pop("__type__")

        if "tzinfo" in dictionary:
            # This is here for a weird bug that was happening
            if dictionary["tzinfo"] is None or dictionary["tzinfo"] in ["None", "tzlocal()", "tzutc()"]:
                dictionary["tzinfo"] = "UTC"

            dictionary["tzinfo"] = pytz.timezone(dictionary["tzinfo"])

        if type_name == "datetime":
            return datetime.datetime(**dictionary)
        elif type_name == "date":
            return datetime.date(**dictionary)
        elif type_name == "time":
            return datetime.time(**dictionary)
        elif type_name == "uuid":
            return uuid.UUID(**dictionary)
        elif type_name == "datetime_range":
            return DateTimeTZRange(**dictionary)
        else:
            dictionary["__type__"] = type_name
            return dictionary


class SysconSerializer:
    def dumps(self, obj):
        return json.dumps(obj, cls=SysconEncoder, separators=(",", ":")).encode("utf-8")

    def loads(self, string):
        return json.loads(string.decode("utf-8"), cls=SysconDecoder)


def dumps(obj, **kwargs):
    return json.dumps(obj, cls=SysconEncoder, **kwargs)


def dump(obj, file_pointer, **kwargs):
    return json.dump(obj, file_pointer, cls=SysconEncoder, **kwargs)


def loads(string, **kwargs):
    return json.loads(string, cls=SysconDecoder, **kwargs)


def load(file_pointer, **kwargs):
    return json.load(file_pointer, cls=SysconDecoder, **kwargs)
