from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
from logger import logger as log

class BikeScooterOrMoto(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeScooterOrMoto

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleBikeScooterOrMoto, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.storage.getTextConstant(textConstant.bikeButtonScooterOrMotoScooter)),
        ).add(KeyboardButton(self.storage.getTextConstant(textConstant.bikeButtonScooterOrMotoMoto))
        )

        await msg.answer(
            ctx = ctx,
            text = self.storage.getTextConstant(textConstant.bikeScooterOrMoto),
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "bikeScooterOrMotoMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeScooterOrMotoMessageDidSent" not in data or data["bikeScooterOrMotoMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        self.storage.logToUserRequest(ctx.from_user,RequestCodingKeys.bikeScooterOrMoto , messageText)

        if messageText == self.storage.getTextConstant(textConstant.bikeButtonScooterOrMotoMoto):
            return self.complete(nextModuleName = MenuModuleName.bikeMotoCategory.get)
        
        if messageText == self.storage.getTextConstant(textConstant.bikeButtonScooterOrMotoScooter):
            return self.complete(nextModuleName = MenuModuleName.bikeScooterCategory.get)

        return self.canNotHandle(data)        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================