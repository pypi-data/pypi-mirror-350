from enum import StrEnum, auto


class TrackIdEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
        return "".join([word.title() for word in name.lower().split("_")])

    DIAGNOSTIC = auto()
    DIAGNOSTIC_SBERHEALTH = auto()
    SECOND_OPINION = auto()
    MEDICAL_TEST_DECRYPTION = auto()
    CONSULTATION = auto()
    DUMMY = auto()
    COMMON_CONSULTATION = auto()
    FINANCIER = auto()
    FINANCIER_GENERIC = auto()
    MULTIMODAL = auto()
