from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.Utils.Utils import dictToList

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log


class BikeScooterCategory(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeScooterCategory

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeScooterCategory, "")

        categoryListSmall = dictToList(storage.getJsonData(storage.path.botContentScooterCategoriesSmallList))
        categoryListBig = dictToList(storage.getJsonData(storage.path.botContentScooterCategoriesBigList))
        categoryList = categoryListSmall + categoryListBig
        categoryMaxLen = max(len(categoryListSmall), len(categoryListBig))

        # TODO: Если количество моделей в списках неодинаково, ты мы огребаем IndexError. Надо что-то с этим придумать.

        keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
        )
        categoryCounter = 0
        while categoryCounter < categoryMaxLen:
            keyboardMarkup.row(KeyboardButton(categoryListSmall[categoryCounter]),KeyboardButton(categoryListBig[categoryCounter]))
            categoryCounter+=1
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeScooterCategory.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ 
                "bikeScooterCategoryDidSent" : True,
                "categoryList" : categoryList
            }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeScooterCategoryDidSent" not in data or data["bikeScooterCategoryDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText in data["categoryList"] and messageText != "Другое":
            log.info(f"Пользователь выбрал {messageText}")
            storage.logToUserRequest(ctx.from_user, f"Модель скутера: {messageText}")
            return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)
        
        if messageText == "Другое":
            log.info(f"Пользователь решил указать другую модель скутера")
            return self.complete(nextModuleName = MenuModuleName.bikeScooterCategoryChoice.get)
        
        # if messageText not in self.menuDict:
        #     return self.canNotHandle(data)

        return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)
        

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