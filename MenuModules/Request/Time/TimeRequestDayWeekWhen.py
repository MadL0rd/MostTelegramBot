from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class TimeRequestDayWeekWhen(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.timeRequestDayWeekWhen

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleTimeRequestDayWeekWhen, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.timeButtonRequestWhenToday.get),
        ).add(KeyboardButton(textConstant.timeButtonRequestWhenTomorrow.get),
        ).add(KeyboardButton(textConstant.timeButtonRequestWhenSetDate.get)
        )
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.timeRequestDayWeekWhen.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "timeRequestDayWeekWhenMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "timeRequestDayWeekWhenMessageDidSent" not in data or data["timeRequestDayWeekWhenMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText == textConstant.timeButtonRequestWhenToday.get:
            log.info("Транспорт нужен сегодня")
            storage.logToUserRequest(ctx.from_user, f"Когда нужен транспорт: {messageText}")
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyDays.get)
        
        if messageText == textConstant.timeButtonRequestWhenTomorrow.get:
            log.info("Транспорт нужен завтра")
            storage.logToUserRequest(ctx.from_user, f"Когда нужен транспорт: {messageText}")
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyDays.get)

        if messageText == textConstant.timeButtonRequestWhenSetDate.get:
            log.info("Выбрал дату")
            return self.complete(nextModuleName = MenuModuleName.timeRequestDayWeekWhenSetDate.get)

        # if messageText not in self.menuDict:
        #     return self.canNotHandle(data)

        return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyDays.get)
        

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
