import enum
from logger import logger as log

class LanguageKey(enum.Enum):

    ru = "ru"
    en = "en"
    
    @staticmethod
    def values() -> list:
        return [language.value for language in LanguageKey]