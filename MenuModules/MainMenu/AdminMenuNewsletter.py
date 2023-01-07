from aiogram.types import Message, CallbackQuery
from main import bot
from logger import logger as log
from Core.GoogleSheetsService import GoogleSheetsService
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.Utils.Utils as utils
from Core.StorageManager.LanguageKey import LanguageKey

from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

from main import bot

class AdminMenuNewsletter(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.adminNewsletter

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        buttons = ["All"] + LanguageKey.values()
        
        keyboardMarkup = utils.replyMarkupFromListOfButtons(buttons)
        
        await msg.answer(
            ctx = ctx,
            text = "Выберите язык сообщения",
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress = True,
            didHandledUserInteraction=True,
            moduleData={ "startMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "language" not in data:
            if ctx.text == "All" or ctx.text in LanguageKey.values():
                data["language"] = ctx.text
                await msg.answer(
                    ctx = ctx,
                    text = "Введите сообщение",
                    keyboardMarkup = ReplyKeyboardRemove()
                )
                return Completion(
                    inProgress=True,
                    didHandledUserInteraction=True,
                    moduleData=data
                )

            return self.canNotHandle(data)

        if "messageText" not in data:
            data["messageText"] = ctx.text
            await msg.answer(
                ctx = ctx,
                text = ctx.text,
                keyboardMarkup = ReplyKeyboardRemove()
            )
            await msg.answer(
                ctx = ctx,
                text = "Проверка сообщения",
                keyboardMarkup = utils.replyMarkupFromListOfButtons(["Начать отправку", "Отмена"])
            )
            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )

        if ctx.text == "Отмена":
            return self.complete(
                nextModuleName = MenuModuleName.admin.value
            )
        
        if ctx.text == "Начать отправку":

            for userFolder in self.storage.path.usersDir.iterdir():
                userId = userFolder.name
                userInfo = self.storage.getUserInfo(userId)

                if data["language"] == "All" or userInfo["language"] == data["language"]:
                    try:
                        await bot.send_message(
                            chat_id = userId,
                            text = data["messageText"]
                        )
                    except Exception as e:
                        log.error(e)

            return self.complete(
                nextModuleName = MenuModuleName.admin.value
            )
            
        return self.canNotHandle(data)


    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================