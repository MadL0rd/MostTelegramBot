from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

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
        self.storage.logToUserHistory(ctx.from_user, event.startModuleTimeRequest, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestDay)),
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestWeek)),
        ).add(KeyboardButton(self.getText(textConstant.timeButtonRequestMonth))
        )

        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.timeRequest),
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
        self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyTimeRequest, messageText)

        if messageText == self.getText(textConstant.timeButtonRequestDay):
            return self.complete(nextModuleName = MenuModuleName.timeRequestDayWeekWhen.get)
        
        if messageText == self.getText(textConstant.timeButtonRequestWeek):
            return self.complete(nextModuleName = MenuModuleName.timeRequestDayWeekWhen.get)

        if messageText == self.getText(textConstant.timeButtonRequestMonth):
            return self.complete(nextModuleName = MenuModuleName.timeRequestHowManyMonths.get)

        return self.canNotHandle(data)

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================      