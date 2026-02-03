import enum
import inspect
from functools import cache

from plantstar_shared import syscon_json
from plantstar_shared.errors import SysconProgrammingError


class SysconType:
    @classmethod
    def _field_iterator(the_class):
        for key, value in inspect.getmembers(the_class()):
            if not key.startswith("__") and not inspect.isfunction(value) and not inspect.ismethod(value):
                yield key, value

    @classmethod
    def get_options(the_class):
        return [value for _, value in the_class._field_iterator()]

    @classmethod
    def convert_to_json(the_class):
        base_dictionary = dict(the_class._field_iterator())

        return syscon_json.dumps(base_dictionary, default=lambda _: "Not Serializeable")


# This is the deprecated version of SysconType, which uses enum.Enum.  It is left here until US#294 https://syscon-intl.monday.com/boards/4307087676/pulses/4414108867 is complete
class SysconTypeOld(enum.Enum):
    @classmethod
    def get_type_tuple_by_type_name(the_class, type_name):
        # Make a `type_cache` for all of the types the first time this method is called.  It may seem strange to not use a `cache` decorator here, but because we know of all the
        # types up front, we don't need to search for and cache each item individually, on every call to the method, which would be less efficient than building the cache up in a
        # single loop.
        if not hasattr(the_class, "_type_cache"):
            the_class._type_cache = {the_type.value[0]: the_type.value for the_type in the_class}

        type_tuple = the_class._type_cache.get(type_name, None)

        if type_tuple is None:
            class_name_singular = the_class.__name__.removesuffix("s")
            option_names = [f"\"{option[0]}\"" for option in the_class.get_options()]
            option_name_string = ", ".join(option_names)
            raise SysconProgrammingError(f"Invalid {class_name_singular}: \"{type_name}\".  Options are: [{option_name_string}]")

        return type_tuple

    @classmethod
    @cache
    def get_options(the_class):
        return [item.value for item in the_class]

    @classmethod
    @cache
    def convert_to_json(the_class):
        base_dictionary = {item.name: item.value for item in the_class}
        return syscon_json.dumps(base_dictionary, default=lambda _: "Not Serializeable")
