import enum
from logger import logger as log

class LanguageKey(enum.Enum):

    ru = "RU"
    en = "EN"
    
    @staticmethod
    def values() -> list:
        return [language.value for language in LanguageKey]