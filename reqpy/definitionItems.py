from enum import StrEnum, auto


class DefintionType(StrEnum):
    ACRONYM = auto()
    DEFINITION = auto()

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        raise ValueError(
                '%r is not a valid %s.  Valid types: %s' % (
                    value,
                    cls.__name__,
                    ', '.join([repr(m.value) for m in cls]),
                    ))