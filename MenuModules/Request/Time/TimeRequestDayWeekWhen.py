from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

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
        self.storage.logToUserHistory(ctx.from_user, event.startModuleTimeRequestDayWeekWhen, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestWhenToday)),
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestWhenTomorrow)),
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestWhenSetDate))
        )

        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.timeRequestDayWeekWhen),
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

        if messageText == self.getText(textConstant.timeButtonRequestWhenToday):
            self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyTimeRequestDayWeekWhen, messageText)
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyDays.get)
        
        if messageText == self.getText(textConstant.timeButtonRequestWhenTomorrow):
            self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyTimeRequestDayWeekWhen, messageText)
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyDays.get)

        if messageText == self.getText(textConstant.timeButtonRequestWhenSetDate):
            return self.complete(nextModuleName = MenuModuleName.timeRequestDayWeekWhenSetDate.get)
            
        return self.canNotHandle(data)
       
    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================