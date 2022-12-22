from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant

from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

from logger import logger as log

class BikeCommitment(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeCommitment

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleBikeCommitment, "")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleStartBikeOrCarChoice, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.getText(textConstant.bikeButtonCommitmentYes)),
        ).add(KeyboardButton(self.getText(textConstant.bikeButtonCommitmentNo))
        )
        
        userTg = ctx.from_user

        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.bikeCommitment),
            keyboardMarkup = keyboardMarkup
        )

        self.storage.updateUserRequest(userTg, {})

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "bikeCommitmentMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeCommitmentMessageDidSent" not in data or data["bikeCommitmentMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepKeyBikeCommitment, self.getText(textConstant.orderStepValueBikeCommitment))

        if messageText == self.getText(textConstant.bikeButtonCommitmentNo):
            await msg.answer(
                ctx = ctx,
                text = self.getText(textConstant.bikeModelsDescription),
                keyboardMarkup=ReplyKeyboardMarkup(
                resize_keyboard=True)
            )
            return self.complete(nextModuleName = MenuModuleName.bikeScooterOrMoto.get)

        if messageText == self.getText(textConstant.bikeButtonCommitmentYes):
            return self.complete(nextModuleName = MenuModuleName.bikeScooterOrMoto.get)

        return self.canNotHandle(data)        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================