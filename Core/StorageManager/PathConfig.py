from pathlib import Path
from aiogram.types import User

from Core.StorageManager.LanguageKey import LanguageKey

class PathConfig:

    languageKey: str

    def __init__(self, language: LanguageKey):
        self.languageKey = language.value
        initFolders = [
            self.baseDir,
            self.usersDir,
            self.botContentDir,
            self.channelOrdersDir
        ]
        for folder in initFolders:
            folder.mkdir(exist_ok=True)

    @property
    def baseDir(self):
        return Path("./DataStorage")
    @property
    def botContentPrivateConfig(self):
        return self.baseDir / "PrivateConfig.json"

    @property
    def usersDir(self):
        return self.baseDir / "Users"

    @property
    def botContentDir(self):
        return self.baseDir / "BotContent" / self.languageKey
    @property
    def botContentOnboarding(self):
        return self.botContentDir / "Onboarding.json"
    @property
    def botContentBikeCriteria(self):
        return self.botContentDir / "BikeCriteria.json"
    @property
    def botContentUniqueMessages(self):
        return self.botContentDir / "UniqueTextMessages.json"
    @property
    def totalHistoryTableFile(self):
        return self.baseDir / "TotalHistory.xlsx"
    @property
    def statisticHistoryTableFile(self):
        return self.baseDir / "StatisticalHistory.xlsx"
    @property
    def botContentScooterCategoriesSmallList(self):
        return self.botContentDir / "ScooterCategoriesSmall.json"
    @property
    def botContentScooterCategoriesBigList(self):
        return self.botContentDir / "ScooterCategoriesBig.json"
    @property
    def botContentMotoCategoriesList(self):
        return self.botContentDir / "MotoCategories.json"

    @property
    def channelOrdersDir(self):
        return self.baseDir / "Orders"

    def orderDir(self, orderId: int):
        return self.channelOrdersDir / f"{orderId}.json"

    def userFolder(self, user: User):
        return self.usersDir / f"{user.id}"

    def userInfoFile(self, user: User):
        return self.userFolder(user) / "info.json"
    
    def userRequestFile(self, user: User):
        return self.userFolder(user) / "request.json"

    def userHistoryFile(self, user: User):
        return self.userFolder(user) / "history.json"