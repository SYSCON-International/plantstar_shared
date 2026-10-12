class AndonLightsKeyConstants:
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    WHITE = "white"
    BUZZER = "buzzer"

    def get_list_of_options(self):
        return [self.RED, self.GREEN, self.YELLOW, self.BLUE, self.WHITE, self.BUZZER]


class AndonLightsStatuses:
    OFF = 0
    ON = 1
    FLASHING = 2

    def get_list_of_options(self):
        return [self.OFF, self.ON, self.FLASHING]


class AndonLightsBuzzerStatuses:
    OFF = 0
    ON_LOUD = 1
    ON_SOFT = 2
    FLASH_LOUD = 3
    FLASH_SOFT = 4

    def get_list_of_options(self):
        return [self.OFF, self.ON_LOUD, self.ON_SOFT, self.FLASH_LOUD, self.FLASH_SOFT]
