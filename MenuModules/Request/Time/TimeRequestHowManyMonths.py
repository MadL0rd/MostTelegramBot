from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

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
        self.storage.logToUserHistory(ctx.from_user, event.startModuleTimeRequestHowManyMonths, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.storage.getTextConstant(textConstant.timeButtonRequestHowManyMonths1)),
        ).add(KeyboardButton(self.storage.getTextConstant(textConstant.timeButtonRequestHowManyMonths2)),
        ).add(KeyboardButton(self.storage.getTextConstant(textConstant.timeButtonRequestHowManyMonths3)),
        ).add(KeyboardButton(self.storage.getTextConstant(textConstant.timeButtonRequestHowManyMonthsMore))
        )
            
        userTg = ctx.from_user
        userInfo = self.storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = self.storage.getTextConstant(textConstant.timeRequestHowManyMonths),
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

        if messageText in [
            self.storage.getTextConstant(textConstant.timeButtonRequestHowManyMonths1), 
            self.storage.getTextConstant(textConstant.timeButtonRequestHowManyMonths2), 
            self.storage.getTextConstant(textConstant.timeButtonRequestHowManyMonths3)
        ]:
            self.storage.logToUserRequest(ctx.from_user, RequestCodingKeys.timeRequestHowManyMonths, messageText)
            return self.complete(nextModuleName = MenuModuleName.timeRequestMonthWhen.get)

        if messageText in (self.storage.getTextConstant(textConstant.timeButtonRequestHowManyMonthsMore)):
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyMonthsSet.get)    

        return self.canNotHandle(data)     

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================