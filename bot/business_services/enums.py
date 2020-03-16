from enum import Enum


class CleaningTypes(Enum):
    SOFT_CLEANING = 0
    CAPITAL_CLEANING = 1
    THOROUGH_CLEANING = 2
    ABSOLUT_CLEANING = 3


class CleaningNames(Enum):
    SOFT_CLEANING = "Легкая уборка"
    CAPITAL_CLEANING = "Капитальная уборка"
    THOROUGH_CLEANING = "Основательная уборка"
    ABSOLUT_CLEANING = "ABSOLUTНАЯ уборка"


class CleaningWindows(Enum):
    WITH_WINDOWS = True
    WITHOUT_WINDOWS = False


class CleaningWindowsNames(Enum):
    WITH_WINDOWS = "Уборка квартиры с помывкой окон (%s руб/м²)"
    WITHOUT_WINDOWS = "Уборка квартиры без помывки окон (%s руб/м²)"


class VisitTypes(Enum):
    DAY_VISIT = 0
    EVENING_VISIT = 1
    NIGHT_VISIT = 2


class VisitNames(Enum):
    DAY_VISIT = "Дневной выезд 9:00 — 15:00 (%s ₽)"
    EVENING_VISIT = "Вечерний выезд 16:00 — 21:00 (%s ₽)"
    NIGHT_VISIT = "Ночной выезд 22:00 — 8:00 (%s ₽)"


class CallbacksTexts(Enum):
    CLEANING_ADDITIONAL_SERVICE_CALLBACK = "cleaning_additional_service.%d"
    ADDITIONAL_SERVICE_ACCEPTED = "additional_service_accepted"
    ADDITIONAL_SERVICE_DECLINED = "additional_service_declined"
    CLEANING_CANCEL = "cleaning_cancel"
    ADDITIONAL_SERVICE_CHOSED = "additional_service_chosed"
