from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.Utils.Utils as utils

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log



class BikeMotoCategory(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeMotoCategory

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeMotoCategory, "")

        categoryDict = storage.getJsonData(storage.path.botContentMotoCategoriesList)
        log.info(categoryDict)
        categoryList = utils.dictToList(categoryDict)
        log.info(categoryList)
        keyboardMarkup = utils.replyMarkupFromListOfButtons(categoryList)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeMotoCategory.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ 
                "bikeMotoCategoryDidSent" : True,
                "categoryList" : categoryList
            }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.info(data["categoryList"])

        if "bikeMotoCategoryDidSent" not in data or data["bikeMotoCategoryDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText in data["categoryList"] and messageText != "Другое":
            log.info(f"Пользователь выбрал {messageText}")
            storage.logToUserRequest(ctx.from_user, f"Категория мотоцикла: {messageText}")
            return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)

        if messageText == "Другое":
            log.info(f"Пользователь решил указать свою модель мотоцилка")
            return self.complete(nextModuleName = MenuModuleName.bikeMotoCategoryChoice.get)

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
                       
        }