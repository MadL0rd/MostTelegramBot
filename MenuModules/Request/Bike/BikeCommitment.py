from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, User

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

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
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeCommitment, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.bikeButtonCommitmentYes.get),
        ).add(KeyboardButton(textConstant.bikeButtonCommitmentNo.get)
        )
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeCommitment.get,
            keyboardMarkup = keyboardMarkup
        )

        storage.updateUserRequest(userTg, [])

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

        storage.logToUserRequest(ctx.from_user, "Тип: Байк")

        if messageText == textConstant.bikeButtonCommitmentNo.get:
            log.info("Юзер запросил описание байков")
            await msg.answer(
                ctx = ctx,
                text = textConstant.bikeModelsDescription.get,
                keyboardMarkup=ReplyKeyboardMarkup(
                resize_keyboard=True)
            )
            return self.complete(nextModuleName = MenuModuleName.bikeScooterOrMoto.get)

        if messageText == textConstant.bikeButtonCommitmentYes.get:
            return self.complete(nextModuleName = MenuModuleName.bikeScooterOrMoto.get)

        if messageText not in self.menuDict:
            return self.canNotHandle(data)

        return log.info("Модуль Commitment завершён"), self.complete(nextModuleName = MenuModuleName.bikeScooterOrMoto.get)
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        return {
            
            textConstant.bikeButtonCommitmentYes.get: MenuModuleName.bikeButtonCommitmentYes.get,
            textConstant.bikeButtonCommitmentNo.get: MenuModuleName.bikeButtonCommitmentNo.get

            
        }