from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant

from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

from logger import logger as log

class GetLicense(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.getLicense

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleGetLicense, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.getText(textConstant.getLicenseButtonCreateOrder)),
        ).add(KeyboardButton(self.getText(textConstant.menuButtonReturnToMainMenu)))

        userTg = ctx.from_user
        
        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.getLicenseText),
            keyboardMarkup = keyboardMarkup
        )
        self.storage.updateUserRequest(userTg, {})
        self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepOrder, self.getText(textConstant.orderStepGetLicense))

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "getLicenseMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "getLicenseMessageDidSent" not in data or data["getLicenseMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText in self.menuDict:
            return self.complete(nextModuleName = self.menuDict[messageText]) 

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
            self.getText(textConstant.getLicenseButtonCreateOrder): MenuModuleName.comment.get,
            self.getText(textConstant.menuButtonReturnToMainMenu): MenuModuleName.mainMenu.get
        }