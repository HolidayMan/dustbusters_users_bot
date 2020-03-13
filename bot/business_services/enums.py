from enum import Enum


class CleaningTypes(Enum):
    SOFT_CLEANING = 0
    CAPITAL_CLEANING = 1
    THOROUGH_CLEANING = 2
    ABSOLUT_CLEANING = 3


class VisitTypes(Enum):
    DAY_VISIT = 0
    EVENING_VISIT = 1
    NIGHT_VISIT = 2
