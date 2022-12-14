from aiogram.types import Message, CallbackQuery
import json
import Core.StorageManager.StorageFactory as storageFactory
from Core.MessageSender import MessageSender
from Core.StorageManager.LanguageKey import LanguageKey
from Core.StorageManager.StorageManager import StorageManager
from Core.StorageManager.UniqueMessagesKeys import UniqueMessagesKeys
from MenuModules.MenuModuleName import MenuModuleName

from logger import logger as log

class MenuModuleHandlerCompletion:

    inProgress: bool
    didHandledUserInteraction: bool
    moduleData: dict
    nextModuleNameIfCompleted: str

    def __init__(self, inProgress: bool, didHandledUserInteraction: bool, moduleData: dict = {}, nextModuleNameIfCompleted: str = ""):
        self.inProgress = inProgress
        self.didHandledUserInteraction = didHandledUserInteraction
        self.moduleData = moduleData
        self.nextModuleNameIfCompleted = nextModuleNameIfCompleted

class MenuModuleInterface:

    namePrivate: MenuModuleName
    languageKey: str
    storage: StorageManager

    def __init__(self, language: LanguageKey):
        self.languageKey = language.value
        self.storage = storageFactory.getStorageForLanguage(language)

    @property
    def name(self) -> str:
        return self.namePrivate.value

    def getText(self, textConstant: UniqueMessagesKeys) -> str:
        return self.storage.getTextConstant(textConstant)

    def callbackData(self, data: dict, msg: MessageSender) -> str:
        data = {
            "module": self.name,
            "data": data
        }
        return json.dumps(data)

    def canNotHandle(self, data: dict) -> MenuModuleHandlerCompletion:
        return MenuModuleHandlerCompletion(
            inProgress=True,
            didHandledUserInteraction=False,
            moduleData=data
        )

    def complete(self, nextModuleName: str = "") -> MenuModuleHandlerCompletion:
        return MenuModuleHandlerCompletion(
            inProgress=False,
            didHandledUserInteraction=True,
            moduleData={},
            nextModuleNameIfCompleted=nextModuleName
        )

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> MenuModuleHandlerCompletion:
        log.error("! Function in menu module does not overrided !")

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> MenuModuleHandlerCompletion:
        log.error(f"! Function in menu module does not overrided !\nData: {data}")

    async def handleCallback(self, ctx: CallbackQuery, msg: MessageSender, data: dict) -> MenuModuleHandlerCompletion:
        log.error(f"! Function in menu module does not overrided ! \nData: {data}")

    