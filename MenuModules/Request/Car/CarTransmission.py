from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

from logger import logger as log

class CarTransmission(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.carTransmission

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleCarTransmission, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).row(KeyboardButton(self.getText(textConstant.carButtonTransmissionAutomatic)), KeyboardButton(self.storage.getTextConstant(textConstant.carButtonTransmissionManual))
        ).add(KeyboardButton(self.getText(textConstant.carButtonTransmissionShowAll))
        )

        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.carTransmission),
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "carTransmissionMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "carTransmissionMessageDidSent" not in data or data["carTransmissionMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyCarTransmission, messageText)
        if messageText in self.menuDict:
            return self.complete(nextModuleName = MenuModuleName.carModels.get)

        return self.canNotHandle(data)
        
    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        return {
            self.getText(textConstant.carButtonTransmissionAutomatic): MenuModuleName.carButtonTransmissionAutomatic.get,
            self.getText(textConstant.carButtonTransmissionManual): MenuModuleName.carButtonTransmissionManual.get,
            self.getText(textConstant.carButtonTransmissionShowAll): MenuModuleName.carButtonTransmissionShowAll.get
        }