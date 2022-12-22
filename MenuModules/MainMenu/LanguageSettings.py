from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Core.StorageManager.LanguageKey import LanguageKey

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant

from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class LanguageSettings(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.languageSettings
    nextModule: MenuModuleName = MenuModuleName.mainMenu

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        for buttonText in self.menuDict:
            keyboardMarkup.add(KeyboardButton(buttonText))

        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.languageSettingsMessageText),
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={}
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        messageText = ctx.text
        if messageText in self.menuDict:

            userTg = ctx.from_user
            userInfo = self.storage.getUserInfo(userTg)
            userInfo["language"] = self.menuDict[messageText]
            self.storage.updateUserData(userTg, userInfo)

            return self.complete(nextModuleName = self.nextModule.get)

        return self.canNotHandle(data)
        
    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================
    
    @property
    def menuDict(self) -> dict:
        return {
            self.getText(textConstant.languageSettingsButtonEn): LanguageKey.en.value,
            self.getText(textConstant.languageSettingsButtonRu): LanguageKey.ru.value
        }