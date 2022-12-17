from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.UniqueMessagesKeys import textConstant

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

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        for buttonText in self.menuDict:
            keyboardMarkup.add(KeyboardButton(buttonText))

        userTg = ctx.from_user
        userInfo = self.storage.getUserInfo(userTg)

        if "isAdmin" in userInfo and userInfo["isAdmin"] == True:
            keyboardMarkup.add(KeyboardButton(self.storage.getTextConstant(textConstant.menuButtonAdmin)))

        await msg.answer(
            ctx = ctx,
            text = self.storage.getTextConstant(textConstant.mainMenuText),
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
        
        messageText = ctx.text
        if messageText == self.storage.getTextConstant(textConstant.menuButtonRentBike):
            return self.complete(nextModuleName = MenuModuleName.bikeCommitment.get)

        if messageText == self.storage.getTextConstant(textConstant.menuButtonRentCar):
            return self.complete(nextModuleName = MenuModuleName.carSize.get)

        if messageText == self.storage.getTextConstant(textConstant.menuButtonAdmin):
            return self.complete(nextModuleName = MenuModuleName.admin.get)

        if messageText == self.storage.getTextConstant(textConstant.menuButtonBuyRights):
            await msg.answer(
                ctx = ctx,
                text = self.storage.getTextConstant(textConstant.menuTextBuyRights),
                keyboardMarkup= ReplyKeyboardRemove()
            )
            return self.complete(nextModuleName= MenuModuleName.mainMenu.get)
        if messageText == self.storage.getTextConstant(textConstant.menuButtonFindInstructor):
            await msg.answer(
                ctx = ctx,
                text = self.storage.getTextConstant(textConstant.menuTextFindInstructor),
                keyboardMarkup= ReplyKeyboardRemove()
            )
            return self.complete(nextModuleName= MenuModuleName.mainMenu.get)

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
            self.storage.getTextConstant(textConstant.menuButtonRentBike): MenuModuleName.rentBike.get,
            self.storage.getTextConstant(textConstant.menuButtonRentCar): MenuModuleName.rentCar.get,
            self.storage.getTextConstant(textConstant.menuButtonBuyRights): MenuModuleName.mainMenu.get,            
            self.storage.getTextConstant(textConstant.menuButtonFindInstructor): MenuModuleName.mainMenu.get
        }