from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Request.RequestCodingKeys import RequestCodingKeys
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
        ).add(KeyboardButton(textConstant.commentCompleteOrderButton.get)
        ).add(KeyboardButton(textConstant.commentUserWishesButton.get))
        
        userRequestString = getUserRequestString(ctx)

        await msg.answer(
            ctx = ctx,
            text = f"{textConstant.commentOrderTextStart.get}\n\n{userRequestString}",
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={}
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        messageText = ctx.text
        if messageText == textConstant.commentUserWishesButton.get:
            await msg.answer(
                ctx = ctx,
                text = textConstant.commentUserWishesText.get,
                keyboardMarkup = ReplyKeyboardRemove()
            )

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData={ "commentMessageDidSent" : True }
            )

        if "commentMessageDidSent" in data and data["commentMessageDidSent"] == True:
            storage.logToUserRequest(ctx.from_user, RequestCodingKeys.comment, messageText)

        if messageText == textConstant.commentCompleteOrderButton.get or "commentMessageDidSent" in data:

            userRequestString = getUserRequestString(ctx)
            userRequestString = f"{ctx.from_user.full_name} @{ctx.from_user.username}\n{userRequestString}"

            await crossDialogMessageSender.setWaitingForOrder(ctx.from_user, userRequestString)

            storage.updateUserRequest(ctx.from_user, {})
            
            await msg.answer(
                ctx = ctx,
                text = textConstant.messageAfterFillingOutForm.get,
                keyboardMarkup = ReplyKeyboardRemove()
            )
            return self.complete(nextModuleName = MenuModuleName.mainMenu.get)    

        return self.canNotHandle(data=data)    

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

def getUserRequestString(ctx: Message) -> str:
    userRequest = storage.getUserRequest(user=ctx.from_user)
    userRequestString = ""
    for line in userRequest.values():
        userRequestString += f"{line['title']}: {line['value']}\n"

    return userRequestString