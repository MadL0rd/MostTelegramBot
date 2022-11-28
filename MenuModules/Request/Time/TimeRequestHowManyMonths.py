from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
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
        ).add(KeyboardButton(textConstant.timeButtonRequestHowManyMonths1.get),
        ).add(KeyboardButton(textConstant.timeButtonRequestHowManyMonths2.get),
        ).add(KeyboardButton(textConstant.timeButtonRequestHowManyMonths3.get),
        ).add(KeyboardButton(textConstant.timeButtonRequestHowManyMonthsMore.get)
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

        if messageText in (
            textConstant.timeButtonRequestHowManyMonths1.get, 
            textConstant.timeButtonRequestHowManyMonths2.get, 
            textConstant.timeButtonRequestHowManyMonths3.get
            ):
            storage.logToUserRequest(ctx.from_user, RequestCodingKeys.timeRequestHowManyMonths, messageText)
            return self.complete(nextModuleName = MenuModuleName.timeRequestMonthWhen.get)

        if messageText in (textConstant.timeButtonRequestHowManyMonthsMore.get):
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyMonthsSet.get)    

        return self.canNotHandle(data)     

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================