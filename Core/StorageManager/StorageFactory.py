from aiogram.types import User

from Core.StorageManager.LanguageKey import LanguageKey
from Core.StorageManager.StorageManager import StorageManager

from logger import logger as log

languageDefault = LanguageKey.en

storages = {}
languages = {}
for language in LanguageKey:
    storages[language.value] = StorageManager(language)
    languages[language.value] = language

storageDefault: StorageManager = storages[languageDefault.value]

def getLanguageForUser(user: User) -> LanguageKey:
    userInfo = storageDefault.getUserInfo(user)

    if "language" not in userInfo or userInfo["language"] not in LanguageKey.values():
        userInfo["language"] = languageDefault.value
        storageDefault.updateUserData(user, userInfo)
        return languageDefault
        
    return languages[userInfo["language"]]

def getStorageForLanguage(language: LanguageKey) -> StorageManager:
    return storages[language.value]

def getStorageForUser(user: User) -> StorageManager:
    return getStorageForLanguage(getLanguageForUser(user))
