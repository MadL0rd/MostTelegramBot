from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

from main import crossDialogMessageSender

# from Core.CrossDialogMessageSender import crossDialogMessageSenderShared

class Comment(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.comment

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleComment, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        userRequest = storage.getUserRequest(user=ctx.from_user)
        userRequestString = textConstant.commentStart.get + "\n"
        for line in userRequest:
            userRequestString += f"{userRequest[line]}\n"
        userRequestString += textConstant.comment.get

        await msg.answer(
            ctx = ctx,
            text = userRequestString,
            keyboardMarkup = keyboardMarkup.add(KeyboardButton("Закончить"))
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "commentMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "commentMessageDidSent" not in data or data["commentMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText != "Закончить":
            storage.logToUserRequest(ctx.from_user,"comment", f"Комментарий: {messageText}")
        
        log.info(messageText)
        
        userRequest = storage.getUserRequest(user=ctx.from_user)
        userRequestString = ""
        for line in userRequest:
            userRequestString += f"{userRequest[line]}\n"


        userRequestString = f"{ctx.from_user.full_name} @{ctx.from_user.username}\n{userRequestString}"

        await crossDialogMessageSender.setWaitingForOrder(ctx.from_user, userRequestString)

        storage.updateUserRequest(ctx.from_user, {})

        # if messageText not in self.menuDict:
        #     return self.canNotHandle(data)
        await msg.answer(
            ctx = ctx,
            text = textConstant.messageAfterFillingOutForm.get,
            keyboardMarkup = ReplyKeyboardRemove()
        )
        return self.complete(nextModuleName = MenuModuleName.mainMenu.get)        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        return {

        }