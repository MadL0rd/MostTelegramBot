from aiogram.types import Message, CallbackQuery

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender
from Core.Utils.Utils import doubleListToButton

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

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
        self.storage.logToUserHistory(ctx.from_user, event.startModuleBikeScooterCategory, "")

        categoryListSmall = self.storage.getJsonData(self.storage.path.botContentScooterCategoriesSmallList)
        categoryListBig = self.storage.getJsonData(self.storage.path.botContentScooterCategoriesBigList)
        categoryList = categoryListSmall + categoryListBig
        textAnything = self.getText(textConstant.orderStepValueOther)
        textSomething = "---------"
        keyboardMarkup = doubleListToButton(categoryListSmall, categoryListBig, textAnything, textSomething)

        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.bikeScooterCategory),
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
            self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyBikeScooterCategory, messageText)
            return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)
        
        if messageText == data["textAnything"]:
            self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyBikeScooterCategory, messageText)
            return self.complete(nextModuleName = MenuModuleName.bikeScooterCategoryChoice.get)
        
        return self.canNotHandle(data)        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================