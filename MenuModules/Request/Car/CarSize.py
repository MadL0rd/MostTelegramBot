from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class CarSize(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.carSize

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleCarSize, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).row(KeyboardButton(textConstant.carButtonSizeSmall.get),KeyboardButton(textConstant.carButtonSizeBig.get)
        ).row(KeyboardButton(textConstant.carButtonSizeMinivan.get),KeyboardButton(textConstant.carButtonSizePremium.get)
        ).add(KeyboardButton(textConstant.carButtonSizeShowAll.get))
        

        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.carSize.get,
            keyboardMarkup = keyboardMarkup
        )
        storage.updateUserRequest(userTg, {})
        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "carSizeMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "carSizeMessageDidSent" not in data or data["carSizeMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        storage.logToUserRequest(ctx.from_user,"carSize" ,f"Размер машины: {messageText}")
        if messageText in self.menuDict:
            log.info(messageText)
            return self.complete(nextModuleName = MenuModuleName.carTransmission.get)
        
            
            

        if messageText not in self.menuDict:
            return self.canNotHandle(data)

        return self.complete(nextModuleName = MenuModuleName.mainMenu.get)
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        return {
            textConstant.carButtonSizeSmall.get: MenuModuleName.carButtonSizeSmall.get,
            textConstant.carButtonSizeBig.get: MenuModuleName.carButtonSizeBig.get,
            textConstant.carButtonSizeMinivan.get: MenuModuleName.carButtonSizeMinivan.get,
            textConstant.carButtonSizePremium.get: MenuModuleName.carButtonSizePremium.get,
            textConstant.carButtonSizeShowAll.get: MenuModuleName.carButtonSizeShowAll.get,
        }