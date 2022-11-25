from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class TimeRequestHowManyMonths(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.timeRequestHowManyMonths

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleTimeRequestHowManyMonths, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton("Один месяц"),
        ).add(KeyboardButton("Два месяца"),
        ).add(KeyboardButton("Три месяца"),
        ).add(KeyboardButton("Больше трёх месяцев")
        )
            
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.timeRequestHowManyMonths.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "timeRequestHowManyMonthsMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "timeRequestHowManyMonthsMessageDidSent" not in data or data["timeRequestHowManyMonthsMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText in ("Один месяц","Два месяца","Три месяца"):
            storage.logToUserRequest(ctx.from_user, "timeRequestHowManyMonths",f"На сколько месяцев аренда: {messageText}")
            log.info(f"Транспорт нужен на {messageText}")
            return self.complete(nextModuleName = MenuModuleName.timeRequestMonthWhen.get)

        if messageText in ("Больше трёх месяцев"):
            log.info(f"Транспорт нужен больше чем на три месяца")
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyMonthsSet.get)    
            
        # if messageText not in self.menuDict:
        #     return self.canNotHandle(data)

        return self.complete(nextModuleName = MenuModuleName.timeRequestMonthWhen.get)
        

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