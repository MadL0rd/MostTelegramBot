from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.Utils.Utils import dictToList

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log


class BikeScooterCategoryChoice(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeScooterCategoryChoice

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeScooterCategoryChoice, "")
        
        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeScooterCategoryChoice.get,
            keyboardMarkup = ReplyKeyboardRemove()
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ 
                "bikeScooterCategoryChoiceMessageDidSent" : True
            }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeScooterCategoryChoiceMessageDidSent" not in data or data["bikeScooterCategoryChoiceMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        storage.logToUserRequest(ctx.from_user,"bikeScooterCategoryChoice", f"Категория скутера: {messageText}")
        log.info(f"Пользователь выбрал свою модель скутера: {messageText}")       
        
        # if messageText not in self.menuDict:
        #     return self.canNotHandle(data)

        return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)
        

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