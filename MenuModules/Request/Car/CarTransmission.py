from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class CarTransmission(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.carTransmission

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleCarTransmission, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).row(KeyboardButton(textConstant.carButtonTransmissionAutomatic.get),KeyboardButton(textConstant.carButtonTransmissionManual.get)
        ).add(KeyboardButton(textConstant.carButtonTransmissionShowAll.get))
        

        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.carTransmission.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "carTransmissionMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "carTransmissionMessageDidSent" not in data or data["carTransmissionMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        storage.logToUserRequest(ctx.from_user, "carTransmission",f"Трансмиссия: {messageText}")
        if messageText in self.menuDict:
            return self.complete(nextModuleName = MenuModuleName.carModels.get)
        
            
            

        if messageText not in self.menuDict:
            return self.canNotHandle(data)

        return self.complete(nextModuleName = MenuModuleName.carModels.get)
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        return {
            textConstant.carButtonTransmissionAutomatic.get: MenuModuleName.carButtonTransmissionAutomatic.get,
            textConstant.carButtonTransmissionManual.get: MenuModuleName.carButtonTransmissionManual.get,
            textConstant.carButtonTransmissionShowAll.get: MenuModuleName.carButtonTransmissionShowAll.get
     
        }