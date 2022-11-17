from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class BikeCriteriaChoice(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeCriteriaChoice

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeCriteriaChoice, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton("Далее")
        )
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeCriteriaChoice.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "bikeCriteriaChoiceMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeCriteriaChoiceMessageDidSent" not in data or data["bikeCriteriaChoiceMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        storage.logToUserRequest(ctx.from_user, f"Критерии байка: {messageText}")

        if messageText == "Далее":
            log.info("Юзер выбрал критерии")
            return self.complete(nextModuleName = MenuModuleName.bikeHelmet.get)

        # TODO: Сделать выбор критериев поиска
        

        # if messageText not in self.menuDict:
        #     return self.canNotHandle(data)

        return log.info("Модуль BikeCriteriaChoice завершён")
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
            
        }