from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class BikeParameters(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeParameters

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleBikeScooterOrMoto, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.getText(textConstant.bikeButtonCriteria))
        ).add(KeyboardButton(self.getText(textConstant.bikeButtonShowAll)))
        
        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.bikeParameters),
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "bikeButtonCriteriaMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeButtonCriteriaMessageDidSent" not in data or data["bikeButtonCriteriaMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText == self.getText(textConstant.bikeButtonCriteria):
            return self.complete(nextModuleName = MenuModuleName.bikeCriteriaChoice.get)
        
        if messageText == self.getText(textConstant.bikeButtonShowAll):
            await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.bikeButtonCriteriaShowAllAnswer),
            keyboardMarkup = ReplyKeyboardMarkup()
        )
            return self.complete(nextModuleName = MenuModuleName.bikeHelmet.get)

        return self.canNotHandle(data)     

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================