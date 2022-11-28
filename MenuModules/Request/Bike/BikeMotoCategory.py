from aiogram.types import Message, CallbackQuery

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.Utils.Utils as utils

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
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
        categoryList = categoryDict
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
                "categoryList" : categoryList
            }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.debug(data["categoryList"])

        messageText = ctx.text

        if messageText in data["categoryList"] and messageText != "Другое":
            storage.logToUserRequest(ctx.from_user, RequestCodingKeys.bikeMotoCategory, messageText)
            return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)

        if messageText == "Другое":
            storage.logToUserRequest(ctx.from_user, RequestCodingKeys.bikeMotoCategory, messageText)
            return self.complete(nextModuleName = MenuModuleName.bikeMotoCategoryChoice.get)

        return self.canNotHandle(data)

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================