from enum import StrEnum, auto


class MTRSXMLTagEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
        return f"mtrs_{name.lower()}"

    NAME = auto()
    LABEL = auto()
    DESC = auto()
