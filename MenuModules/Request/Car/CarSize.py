from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
from logger import logger as log

class CarSize(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.carSize

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleCarSize, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).row(KeyboardButton(self.storage.getTextConstant(textConstant.carButtonSizeSmall.get),KeyboardButton(textConstant.carButtonSizeBig))
        ).row(KeyboardButton(self.storage.getTextConstant(textConstant.carButtonSizeMinivan.get),KeyboardButton(textConstant.carButtonSizePremium))
        ).add(KeyboardButton(self.storage.getTextConstant(textConstant.carButtonSizeShowAll)))
        
        userTg = ctx.from_user

        await msg.answer(
            ctx = ctx,
            text = self.storage.getTextConstant(textConstant.carSize),
            keyboardMarkup = keyboardMarkup
        )
        self.storage.updateUserRequest(userTg, {})
        self.storage.logToUserRequest(ctx.from_user,RequestCodingKeys.carCommitment, "Авто")

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "carSizeMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "carSizeMessageDidSent" not in data or data["carSizeMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        self.storage.logToUserRequest(ctx.from_user, RequestCodingKeys.carSize , messageText)
        if messageText in self.menuDict:
            log.info(messageText)
            return self.complete(nextModuleName = MenuModuleName.carTransmission.get)
        else:
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
            self.storage.getTextConstant(textConstant.carButtonSizeSmall): MenuModuleName.carButtonSizeSmall.get,
            self.storage.getTextConstant(textConstant.carButtonSizeBig): MenuModuleName.carButtonSizeBig.get,
            self.storage.getTextConstant(textConstant.carButtonSizeMinivan): MenuModuleName.carButtonSizeMinivan.get,
            self.storage.getTextConstant(textConstant.carButtonSizePremium): MenuModuleName.carButtonSizePremium.get,
            self.storage.getTextConstant(textConstant.carButtonSizeShowAll): MenuModuleName.carButtonSizeShowAll.get,
        }