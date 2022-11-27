from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
from logger import logger as log

class BikeScooterOrMoto(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeScooterOrMoto

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeScooterOrMoto, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.bikeButtonScooterOrMotoScooter.get),
        ).add(KeyboardButton(textConstant.bikeButtonScooterOrMotoMoto.get)
        )
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeScooterOrMoto.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "bikeScooterOrMotoMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeScooterOrMotoMessageDidSent" not in data or data["bikeScooterOrMotoMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        storage.logToUserRequest(ctx.from_user,RequestCodingKeys.bikeScooterOrMoto , messageText)


        if messageText == textConstant.bikeButtonScooterOrMotoMoto.get:
            log.info("Юзер выбрал скутер")
            return self.complete(nextModuleName = MenuModuleName.bikeMotoCategory.get)
        
        if messageText == textConstant.bikeButtonScooterOrMotoScooter.get:
            log.info("Юзер выбрал мотоцикл")
            return self.complete(nextModuleName = MenuModuleName.bikeScooterCategory.get)

        if messageText not in self.menuDict:
            return self.canNotHandle(data)

        return log.info("Модуль BikeScooterOrMoto завершён")
        # self.complete(nextModuleName = self.menuDict[messageText])
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        return {
            
            textConstant.bikeButtonScooterOrMotoMoto.get: MenuModuleName.bikeButtonScooterOrMotoMoto.get,
            textConstant.bikeButtonScooterOrMotoScooter.get: MenuModuleName.bikeButtonScooterOrMotoScooter.get

            
        }