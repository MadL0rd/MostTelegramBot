from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
from logger import logger as log

class TimeRequestMonthWhenSetDate(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.timeRequestMonthWhenSetDate

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleTimeRequestMonthWhenSetDate, "")
        
        await msg.answer(
            ctx = ctx,
            text = textConstant.timeRequestMonthWhenSetDate.get,
            keyboardMarkup = ReplyKeyboardRemove()
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "timeRequestMonthWhenSetDateMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "timeRequestMonthWhenSetDateMessageDidSent" not in data or data["timeRequestMonthWhenSetDateMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        storage.logToUserRequest(ctx.from_user, RequestCodingKeys.timeRequestMonthWhenSetDate, messageText)
        log.info(f"Транспорт нужен на {messageText}")
        return self.complete(nextModuleName = MenuModuleName.requestGeoposition.get)

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================