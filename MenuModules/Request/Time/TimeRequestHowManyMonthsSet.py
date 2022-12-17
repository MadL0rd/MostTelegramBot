from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
from logger import logger as log

class TimeRequestHowManyMonthsSet(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.timeRequestHowManyMonthsSet

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleTimeRequestHowManyMonthsSet, "")

        await msg.answer(
            ctx = ctx,
            text = self.storage.getTextConstant(textConstant.timeRequestHowManyMonthsSet),
            keyboardMarkup = ReplyKeyboardRemove()
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "timeRequestHowManyMonthsSetMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "timeRequestHowManyMonthsSetMessageDidSent" not in data or data["timeRequestHowManyMonthsSetMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        self.storage.logToUserRequest(ctx.from_user, RequestCodingKeys.timeRequestHowManyMonthsSet, messageText)
        return self.complete(nextModuleName = MenuModuleName.timeRequestMonthWhen.get)
        
    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================