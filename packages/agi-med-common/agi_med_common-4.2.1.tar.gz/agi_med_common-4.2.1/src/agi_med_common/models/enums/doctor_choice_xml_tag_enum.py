from enum import StrEnum, auto


class DoctorChoiceXMLTagEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
        return f"{name.lower()}"

    DIAGNOSTICS = auto()
    SUMMARIZATION = auto()
    MTRS = auto()
