from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender
from Core.Utils.Utils import dictToList

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

from logger import logger as log

class BikeMotoCategoryChoice(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeMotoCategoryChoice

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.strartModuleBikeMotoCategoryChoice, "")
        
        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.bikeMotoCategoryChoice),
            keyboardMarkup = ReplyKeyboardRemove()
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ 
                "bikeMotoCategoryChoiceMessageDidSent" : True
            }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeMotoCategoryChoiceMessageDidSent" not in data or data["bikeMotoCategoryChoiceMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyBikeMotoCategoryChoice , messageText)
        return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)
        
    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================