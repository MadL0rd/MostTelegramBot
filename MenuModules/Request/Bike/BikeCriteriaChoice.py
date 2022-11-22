from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class BikeCriteriaChoice(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.bikeCriteriaChoice

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleBikeCriteriaChoice, "")
        
        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        await msg.answer(
            ctx = ctx,
            text = textConstant.bikeCriteriaChoice.get,
            keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
        ).add(KeyboardButton("Приступим"))
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ 
                "bikeCriteriaChoiceMessageDidSent" : True
                }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "bikeCriteriaChoiceMessageDidSent" not in data or data["bikeCriteriaChoiceMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text
        pull = storage.getJsonData(storage.PathConfig.botContentBikeCriteria)
        for line in pull:
            if line["type"] not in data:
                keyboardMarkup = ReplyKeyboardMarkup(
                    resize_keyboard=True
                    )
                for i in range(1,len(line)):
                    keyboardMarkup.add(KeyboardButton(line[f"criteria{i}"]))
                await msg.answer(
                    ctx = ctx,
                    text = line["type"],
                    keyboardMarkup = keyboardMarkup
                    )
                criteriaName = line["type"]
                if messageText != "Приступим":
                    storage.logToUserRequest(ctx.from_user, f"Критерий байка {data['prevCriteria']}: {messageText}")
                data[f"{criteriaName}"] = True
                data["prevCriteria"] = criteriaName
                log.info(data)
                return Completion(
                    inProgress=True,
                    didHandledUserInteraction= True,
                    moduleData=data
                    )
        storage.logToUserRequest(ctx.from_user, f"Критерий байка {data['prevCriteria']}: {messageText}")
        return self.complete(nextModuleName = MenuModuleName.bikeHelmet.get)
        

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