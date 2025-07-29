from enum import StrEnum, auto


class DiagnosticsXMLTagEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
        return f"diag_{name.lower()}"

    DIAG = auto()
    DOC = auto()
    DESC = auto()
