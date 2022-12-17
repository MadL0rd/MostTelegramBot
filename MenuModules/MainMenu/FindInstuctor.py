from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant

from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

from logger import logger as log

class FindInstructor(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.findInstructor

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleFindInstructor, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(self.getText(textConstant.findInstructorButtonCreateOrder)),
        ).add(KeyboardButton(self.getText(textConstant.menuButtonReturnToMainMenu)))

        userTg = ctx.from_user
        
        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.findInstructorText),
            keyboardMarkup = keyboardMarkup
        )
        self.storage.updateUserRequest(userTg, {})
        self.storage.logToUserRequest(ctx.from_user, textConstant.orderStepOrder, self.getText(textConstant.orderStepFindInstructor))

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "findInstructorMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "findInstructorMessageDidSent" not in data or data["findInstructorMessageDidSent"] != True:
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
            self.getText(textConstant.findInstructorButtonCreateOrder): MenuModuleName.comment.get,
            self.getText(textConstant.menuButtonReturnToMainMenu): MenuModuleName.mainMenu.get
        }