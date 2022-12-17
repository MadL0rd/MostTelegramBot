from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

from logger import logger as log

class TimeRequestMonthWhen(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.timeRequestMonthWhen

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuletimeRequestMonthWhen, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestMonthWhenToday)),
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestMonthWhenTomorrow)),
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestMonthWhenComingDays)),
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestMonthWhenSetDate))
        )

        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.timeRequestMonthWhen),
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "timeRequestMonthWhenMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "timeRequestMonthWhenMessageDidSent" not in data or data["timeRequestMonthWhenMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        if messageText in [
            self.getText(textConstant.timeButtonRequestMonthWhenToday),
            self.getText(textConstant.timeButtonRequestMonthWhenTomorrow), 
            self.getText(textConstant.timeButtonRequestMonthWhenComingDays)
        ]:
            self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyTimeRequestMonthWhen, messageText)
            return self.complete(nextModuleName = MenuModuleName.requestGeoposition.get)

        if messageText == (self.getText(textConstant.timeButtonRequestMonthWhenSetDate)):
            return self.complete(nextModuleName = MenuModuleName.timeRequestMonthWhenSetDate.get)
        
        return self.canNotHandle(data)        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================