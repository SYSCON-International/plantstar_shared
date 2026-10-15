from plantstar_shared.SysconType import SysconType


class AndonLightsKeyConstants(SysconType):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    WHITE = "white"
    BUZZER = "buzzer"


class AndonLightsStatuses(SysconType):
    OFF = 0
    ON = 1
    FLASHING = 2


class AndonLightsBuzzerStatuses(SysconType):
    OFF = 0
    ON_LOUD = 1
    ON_SOFT = 2
    FLASH_LOUD = 3
    FLASH_SOFT = 4
