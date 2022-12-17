from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.Utils.Utils as utils

from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class MainMenu(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.mainMenu

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        self.storage.logToUserHistory(ctx.from_user, event.startModuleMainMenu, "")

        userTg = ctx.from_user
        userInfo = self.storage.getUserInfo(userTg)

        buttons = [button for button in self.menuDict]
        if "isAdmin" in userInfo and userInfo["isAdmin"] == True:
            buttons.append(self.getText(textConstant.menuButtonAdmin))

        keyboardMarkup = utils.replyMarkupFromListOfButtons(buttons)

        await msg.answer(
            ctx = ctx,
            text = self.getText(textConstant.mainMenuText),
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "startMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "startMessageDidSent" not in data or data["startMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)

        userTg = ctx.from_user
        userInfo = self.storage.getUserInfo(userTg)

        messageText = ctx.text

        if messageText == self.storage.getTextConstant(textConstant.menuButtonAdmin) and "isAdmin" in userInfo and userInfo["isAdmin"] == True:
            return self.complete(nextModuleName = MenuModuleName.admin.get)
        
        if messageText in self.menuDict:
            # TODO: replace with menu modules
            if messageText == self.getText(textConstant.menuButtonBuyRights):
                await msg.answer(
                    ctx = ctx,
                    text = self.getText(textConstant.menuTextBuyRights),
                    keyboardMarkup= ReplyKeyboardRemove()
                )
                return self.complete(nextModuleName = MenuModuleName.mainMenu.get)
            if messageText == self.getText(textConstant.menuButtonFindInstructor):
                await msg.answer(
                    ctx = ctx,
                    text = self.getText(textConstant.menuTextFindInstructor),
                    keyboardMarkup= ReplyKeyboardRemove()
                )
                return self.complete(nextModuleName= MenuModuleName.mainMenu.get)

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
            self.getText(textConstant.menuButtonRentBike): MenuModuleName.rentBike.get,
            self.getText(textConstant.menuButtonRentCar): MenuModuleName.rentCar.get,
            self.getText(textConstant.menuButtonBuyRights): MenuModuleName.mainMenu.get,            
            self.getText(textConstant.menuButtonFindInstructor): MenuModuleName.mainMenu.get,
            self.getText(textConstant.menuButtonLanguageSettings): MenuModuleName.languageSettings.get
        }