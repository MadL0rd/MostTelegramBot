from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class TimeRequest(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.timeRequest

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleTimeRequest, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.timeButtonRequestDay.get),
        ).add(KeyboardButton(textConstant.timeButtonRequestWeek.get),
        ).add(KeyboardButton(textConstant.timeButtonRequestMonth.get)
        )
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.timeRequest.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "timeRequestMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "timeRequestMessageDidSent" not in data or data["timeRequestMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText == textConstant.timeButtonRequestDay.get:
            log.info("Юзер решил выбирать по дням")
            return self.complete(nextModuleName = MenuModuleName.timeRequestDayWeekWhen.get)
        
        if messageText == textConstant.timeButtonRequestWeek.get:
            log.info("Юзер решил выбирать по неделям")
            return self.complete(nextModuleName = MenuModuleName.timeRequestDayWeekWhen.get)

        if messageText == textConstant.timeButtonRequestMonth.get:
            log.info("Юзер решил выбирать по месяцам")
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyMonths.get)

        if messageText not in self.menuDict:
            return self.canNotHandle(data)

        return log.info("Модуль TimeRequest завершён")
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
            
            textConstant.timeButtonRequestDay.get: MenuModuleName.timeButtonRequestDay.get,
            textConstant.timeButtonRequestWeek.get: MenuModuleName.timeButtonRequestWeek.get,
            textConstant.timeButtonRequestMonth.get: MenuModuleName.timeButtonRequestMonth.get

        }


            
        