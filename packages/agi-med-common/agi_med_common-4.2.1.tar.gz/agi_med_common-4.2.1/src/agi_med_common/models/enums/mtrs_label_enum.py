from enum import StrEnum, auto


class MTRSLabelEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
        return name.upper()

    LABORATORY = auto()
    INSTRUMENTAL = auto()
