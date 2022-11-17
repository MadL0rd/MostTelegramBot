from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
from Core.Utils.Utils import dictToList

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log



class BikeMotoCategory(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeMotoCategory

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeMotoCategory, "")

        categoryList = dictToList(storage.getJsonData(storage.path.botContentMotoCategoriesList))
        categoryLen = len(categoryList)

        keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
        )
        categoryCounter = 0
        while categoryCounter < categoryLen:
            keyboardMarkup.add(KeyboardButton(categoryList[categoryCounter]))
            categoryCounter+=1
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeMotoCategory.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "bikeMotoCategoryDidSent" : True,
                         "categoryList" : categoryList
            
            }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeMotoCategoryDidSent" not in data or data["bikeMotoCategoryDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        storage.logToUserRequest(ctx.from_user, f"Категория мотоцикла: {messageText}")

        if messageText in data["categoryList"]:
            log.info(f"Пользователь выбрал {messageText}")
            return self.complete(nextModuleName = MenuModuleName.bikeParameters.get)

        # TODO: При выборе варианта "другое" надо запрашивать модель и сохранять

        # if messageText not in self.menuDict:
        #     return self.canNotHandle(data)

        return log.info("Модуль BikeMotoCategory завершён")
        # self.complete(nextModuleName = self.menuDict[messageText])
        

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