from aiogram.types import Message, CallbackQuery

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.Utils.Utils import doubleListToButton

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
from logger import logger as log

class BikeScooterCategory(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeScooterCategory

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeScooterCategory, "")

        categoryListSmall = storage.getJsonData(storage.path.botContentScooterCategoriesSmallList)
        categoryListBig = storage.getJsonData(storage.path.botContentScooterCategoriesBigList)
        categoryList = categoryListSmall + categoryListBig
        textAnything = "Другое"
        textSomething = "---------"
        keyboardMarkup = doubleListToButton(categoryListSmall, categoryListBig, textAnything, textSomething)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeScooterCategory.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ 
                "bikeScooterCategoryMessageDidSent" : True,
                "textAnything" : textAnything,
                "categoryList" : categoryList
            }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeScooterCategoryMessageDidSent" not in data or data["bikeScooterCategoryMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText in data["categoryList"] and messageText != data["textAnything"]:
            storage.logToUserRequest(ctx.from_user,RequestCodingKeys.bikeScooterCategory, messageText)
            return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)
        
        if messageText == data["textAnything"]:
            storage.logToUserRequest(ctx.from_user,RequestCodingKeys.bikeScooterCategory, messageText)
            return self.complete(nextModuleName = MenuModuleName.bikeScooterCategoryChoice.get)
        
        return self.canNotHandle(data)        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================