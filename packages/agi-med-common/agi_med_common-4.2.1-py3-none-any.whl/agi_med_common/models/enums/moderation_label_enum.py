from enum import IntEnum, auto


class ModerationLabelEnum(IntEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return count

    OK = auto()
    NON_MED = auto()
    CHILD = auto()
    ABSURD = auto()
    GREETING = auto()
    RECEIPT = auto()
