class AndonLightsKeyConstants:
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    WHITE = "white"
    BUZZER = "buzzer"

    @classmethod
    def get_list_of_options(the_class):
        return [the_class.RED, the_class.GREEN, the_class.YELLOW, the_class.BLUE, the_class.WHITE, the_class.BUZZER]


class AndonLightsStatuses:
    OFF = 0
    ON = 1
    FLASHING = 2

    @classmethod
    def get_list_of_options(the_class):
        return [the_class.OFF, the_class.ON, the_class.FLASHING]


class AndonLightsBuzzerStatuses:
    OFF = 0
    ON_LOUD = 1
    ON_SOFT = 2
    FLASH_LOUD = 3
    FLASH_SOFT = 4

    @classmethod
    def get_list_of_options(the_class):
        return [the_class.OFF, the_class.ON_LOUD, the_class.ON_SOFT, the_class.FLASH_LOUD, the_class.FLASH_SOFT]
