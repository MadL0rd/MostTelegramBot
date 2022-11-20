from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class BikeParameters(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeParameters

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeScooterOrMoto, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.bikeButtonCriteria.get)
        ).add(KeyboardButton(textConstant.bikeButtonShowAll.get))
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeParameters.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "bikeButtonCriteriaMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeButtonCriteriaMessageDidSent" not in data or data["bikeButtonCriteriaMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText == textConstant.bikeButtonCriteria.get:
            log.info("Юзер выбрал выбор критериев")
            return self.complete(nextModuleName = MenuModuleName.bikeCriteriaChoice.get)
        
        if messageText == textConstant.bikeButtonShowAll.get:
            log.info("Юзер решил не выбирать критерии")
            return self.complete(nextModuleName = MenuModuleName.bikeHelmet.get)

        if messageText not in self.menuDict:
            return self.canNotHandle(data)

        return log.info("Модуль BikeParameters завершён")
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
            
            textConstant.bikeButtonCriteria.get: MenuModuleName.bikeButtonCriteria.get,
            textConstant.bikeCriteriaChoice.get: MenuModuleName.bikeButtonShowAll.get

            
        }